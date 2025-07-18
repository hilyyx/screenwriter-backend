from string import Template
from networkx import DiGraph
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque

from lib.llm.settings import LLMSettings

import networkx as nx
import os
import json
import copy

load_dotenv()

def graph_to_JSON(dialog_graph):
        structure = {"data": []}
        for node in list(dialog_graph.nodes):
            structure["data"].append(dialog_graph.nodes[node])
            structure["data"][-1]["id"] = node
            structure["data"][-1]["to"] = []
            for next_node in list(dialog_graph.adj[node].keys()):
                structure["data"][-1]["to"].append(dialog_graph.edges[(node, next_node)])
                structure["data"][-1]["to"][-1]["id"] = next_node
        return structure

def JSON_to_graph(structure):
    dialog_graph = nx.DiGraph()
    for node in structure['data']:
        # print(node)
        dialog_graph.add_node(node["id"], **node)
        for child in node['to']:
            dialog_graph.add_edge(node["id"], child["id"], **child)
    return dialog_graph

class Orchestrator:
    def __init__(self, params: dict):
        self.params = params
    
    def create_dialog(self):
        dialog_generator = DialogGenerator(self.params)
        dialog_validator = DialogValidator(self.params)
        dialog_regenerator = DialogRegenerator(self.params)
        dialog_graph = JSON_to_graph(dialog_generator.generate_structure())
        print("--Структура до валидации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")
        structure_validation = dialog_validator.validate_structure(dialog_graph)
        while not structure_validation[0]:
            dialog_graph = JSON_to_graph(dialog_regenerator.regenerate_structure(dialog_graph, structure_validation[1]))
            print("--Структура в процессе валидации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")
            structure_validation = dialog_validator.validate_structure(dialog_graph)
        print("--Структура после валидации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")
        dialog_generator.generate_content(dialog_graph)   
        print("--Контент до валидации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")
        dialog_validator.validate_content(dialog_graph)
        print(graph_to_JSON(dialog_graph))
        print("--Контент после валидации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")
        dialog_regenerator.regenerate_content(dialog_validator, dialog_graph)
        print("--Контент после перегенерации--", graph_to_JSON(dialog_graph), sep = "\n", end = "\n\n=====\n\n")

class DialogSettings:
    def __init__(self, params: dict):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.structure_model_type = os.getenv("MODEL_TYPE_STRUCTURE")
        self.structure_model_max_tokens = int(os.getenv("STRUCTURE_MODEL_MAX_TOKENS", 8192))
        self.dialogue_model_type = os.getenv("MODEL_TYPE_DIALOGUE")
        self.dialogue_model_max_tokens = int(os.getenv("DIALOGUE_MODEL_MAX_TOKENS", 8192))
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

        self.params = params
        self.npc = self.params["npc"]
        self.hero = self.params["hero"]
        self.goals = self.params["goals"]
        self.llm_settings = LLMSettings()
    
class DialogGenerator(DialogSettings):

    def generate_structure(self):
        with open("resources/prompt_structure.txt", encoding='utf-8', mode="r") as prompt_structure:
            prompt_structure = Template(prompt_structure.read()).safe_substitute(
                json_structure=self.llm_settings.get_structure(),
                json_node_structure=self.llm_settings.get_node_structure(),
                NPC_name=self.npc["name"],
                NPC_talk_style=self.npc["talk_style"],
                NPC_profession=self.npc["profession"],
                NPC_look=self.npc["look"],
                NPC_traits=self.npc["traits"],
                NPC_extra=self.npc["extra"],
                hero_name=self.hero["name"],
                hero_talk_style=self.hero["talk_style"],
                hero_profession=self.hero["profession"],
                hero_look=self.hero["look"],
                hero_extra=self.hero["extra"],
                hero_traits=self.hero["traits"],
                NPC_to_hero_relation=self.params["NPC_to_hero_relation"],
                hero_to_NPC_relation=self.params["hero_to_NPC_relation"],
                world_settings=self.params["world_settings"],
                scene = self.params["scene"],
                genre = self.params["genre"],
                epoch = self.params["epoch"],
                tonality = self.params["tonality"],
                extra = self.params["extra"],
                context = self.params["context"],
                mx_answers_cnt=self.params["mx_answers_cnt"],
                mn_answers_cnt=self.params["mn_answers_cnt"],
                mx_depth=self.params["mx_depth"],
                mn_depth=self.params["mn_depth"],
                moods_list=self.llm_settings.get_moods(),
                goals=self.goals
                )

        structure_response = self.client.chat.completions.create(
            model=self.dialogue_model_type,
            messages=[
                {"role": "system", "content": self.llm_settings.get_system_prompt()},
                {"role": "user", "content": prompt_structure},
            ],
            stream=False,
            max_tokens=self.structure_model_max_tokens,
            temperature=0.6,
            top_p=0.95,
            response_format={
                'type': 'json_object'
            }
        )
        structure = json.loads(structure_response.choices[0].message.content)
        return structure

    def generate_content(self, dialog_graph):
        q = deque()
        start_node = list(dialog_graph.nodes)[0]
        q.append(start_node)
        while q:
            t = q.popleft()
            next_replics = []
            prev_chains = []
            paths = list(nx.all_simple_paths(dialog_graph, source=start_node, target=t))
            next_nodes = list(dialog_graph.adj[t].keys())
            lst_node = -1
            for path in paths:
                dialog_chain = ""
                for ind in range(0, len(path)):
                    node = path[ind]
                    if ind < len(path) - 1:
                        dialog_chain += f'**NPC**: {dialog_graph.nodes[node]["info"]}\n'
                    if ind:
                        dialog_chain += f'**Игрок**: {dialog_graph.edges[lst_node, node]["line"]}\n'
                    lst_node = node
                prev_chains.append(dialog_chain)
            for next_node in next_nodes:
                next_replics.append(dialog_graph.nodes[next_node]["info"])
                if next_node not in q:
                    q.append(next_node)
            with open("resources/prompt_nodes_content.txt", encoding='utf-8', mode="r") as prompt_nodes_content:
                prompt_nodes_content = Template(prompt_nodes_content.read()).safe_substitute(
                    chain="\n = = = = \n".join(prev_chains),
                    tematic=dialog_graph.nodes[t]["info"],
                    world_settings=self.params["world_settings"],
                    name=self.npc["name"],
                    talk_style=self.npc["talk_style"],
                    profession=self.npc["profession"],
                    traits=self.npc["traits"],
                    scene=self.params["scene"],
                    extra=self.params["extra"],
                    look=self.npc["look"],
                    mood=dialog_graph.nodes[t]["mood"],
                    relation=self.params["NPC_to_hero_relation"]
                )
            node_content_response = self.client.chat.completions.create(
                model=self.dialogue_model_type,
                messages=[
                    {"role": "system", "content": self.llm_settings.get_system_prompt()},
                    {"role": "user", "content": prompt_nodes_content},
                ],
                stream=False,
                max_tokens=self.structure_model_max_tokens
            )
            dialog_graph.nodes[t]["line"] = node_content_response.choices[0].message.content.strip("\"\'")
            for i in range(0, len(prev_chains)):
                prev_chains[i] += f'**NPC**: {dialog_graph.nodes[t]["line"]}\n'
            with open("resources/prompt_edges_content.txt", encoding='utf-8', mode="r") as prompt:
                prompt_edges_content = Template(prompt.read()).safe_substitute(
                    json_edge_structure=self.llm_settings.get_edge_structure(),
                    chain="\n = = = = \n".join(prev_chains),
                    tematics="\n = = = = \n".join(next_replics),
                    replic_cnt=len(next_replics),
                    world_settings=self.params["world_settings"],
                    name=self.hero["name"],
                    talk_style=self.hero["talk_style"],
                    profession=self.hero["profession"],
                    traits=self.hero["traits"],
                    look=self.hero["look"],
                    hero_extra=self.hero["extra"],
                    mood=dialog_graph.nodes[t]["mood"],
                    extra=self.params["extra"],
                    scene=self.params["scene"],
                    relation=self.params["hero_to_NPC_relation"]
                )
            edge_content_response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.llm_settings.get_system_prompt()},
                    {"role": "user", "content": prompt_edges_content},
                ],
                stream=False,
                response_format={
                    'type': 'json_object'
                }
            )
            edges_meta = json.loads(edge_content_response.choices[0].message.content)["lines"]
            print("--answers--")
            print(edges_meta)
            for i in range(0, len(next_replics)):
                for key in edges_meta[i].keys():
                    dialog_graph.edges[t, next_nodes[i]][key] = edges_meta[i][key].strip("\"\'")
        return dialog_graph

class DialogValidator(DialogSettings):

    def interpret_rate(self, rate_result):
        metrics_avg = 0
        metrics_mn = -1
        # comments = {}
        for metric in rate_result.keys():
            if metrics_mn == -1 or rate_result[metric]["rate"] < metrics_mn:
                metrics_mn = rate_result[metric]["rate"]
            metrics_avg += rate_result[metric]["rate"]
            # comments[metric] = rate_result[metric]["comment"]
        metrics_avg /= len(rate_result)
        if metrics_mn < 6 or metrics_avg < 7:
            return (0, rate_result)
        return (1, rate_result)
    
    def validate_connectivity(self, dialog_graph, node = None, used = []):
        if node is None:
            node = list(dialog_graph.nodes)[0]
        used.append(node)
        for next_node in list(dialog_graph.adj[node].keys()):
            if next_node not in used:
                self.validate_connectivity(dialog_graph, next_node, used)
        return used
    
    def validate_nodes_type(self, dialog_graph, node = None, used = [], mTypeCnt = 0):
        if node is None:
            node = list(dialog_graph.nodes)[0]
        used.append(node)
        curType = ""
        if len(list(dialog_graph.adj[node].keys())) == 0:
            curType = 'P'
            mTypeCnt = 0
        elif len(list(dialog_graph.adj[node].keys())) == 1:
            curType = 'M'
            mTypeCnt+=1
        else:
            curType = 'C'
            mTypeCnt = 0
        dialog_graph.nodes[node]["type"] = curType
        # print(node, mTypeCnt)
        if mTypeCnt == 3:
            next_node = list(dialog_graph.adj[node].keys())[0]
            for edge in dialog_graph.in_edges(node):
                if (edge[0], next_node) not in dialog_graph.in_edges(next_node):
                    dialog_graph.add_edge(edge[0], next_node, **dict(dialog_graph.edges[edge]))
            dialog_graph.remove_node(node)
            mTypeCnt = 2
            self.validate_nodes_type(dialog_graph, next_node, used, mTypeCnt)
        else:
            for next_node in list(dialog_graph.adj[node].keys()):
                if next_node not in used:
                    self.validate_nodes_type(dialog_graph, next_node, used, mTypeCnt)
    

    def validate_structure_alg(self, dialog_graph):
        used = self.validate_connectivity(dialog_graph)
        for node in list(dialog_graph.nodes):
            if node not in used:
                dialog_graph.remove_node(node)
        self.validate_nodes_type(dialog_graph)
        return dialog_graph
    def validate_structure_llm(self, structure):
        with open("resources/prompt_structure_validation.txt", encoding = 'utf-8', mode= "r") as prompt_edges_content:
            prompt_structure_validation = Template(prompt_edges_content.read()).safe_substitute(
                json_structure=self.llm_settings.get_structure(),
                json_node_structure=self.llm_settings.get_node_structure(),
                NPC_name=self.npc["name"],
                NPC_talk_style=self.npc["talk_style"],
                NPC_profession=self.npc["profession"],
                NPC_look=self.npc["look"],
                NPC_traits=self.npc["traits"],
                NPC_extra=self.npc["extra"],
                hero_name=self.hero["name"],
                hero_talk_style=self.hero["talk_style"],
                hero_profession=self.hero["profession"],
                hero_look=self.hero["look"],
                hero_extra=self.hero["extra"],
                hero_traits=self.hero["traits"],
                NPC_to_hero_relation=self.params["NPC_to_hero_relation"],
                hero_to_NPC_relation=self.params["hero_to_NPC_relation"],
                world_settings=self.params["world_settings"],
                scene = self.params["scene"],
                genre = self.params["genre"],
                epoch = self.params["epoch"],
                tonality = self.params["tonality"],
                extra = self.params["extra"],
                context = self.params["context"],
                mx_answers_cnt=self.params["mx_answers_cnt"],
                mn_answers_cnt=self.params["mn_answers_cnt"],
                mx_depth=self.params["mx_depth"],
                mn_depth=self.params["mn_depth"],
                moods_list=self.llm_settings.get_moods(),
                goals=self.goals,
                structure = structure,
                json_metrics = self.llm_settings.get_json_metrics()
        )
        structure_validation_response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": self.llm_settings.get_system_prompt()},
                {"role": "user", "content": prompt_structure_validation},
            ],
            stream=False,
            max_tokens=20000,
            response_format={
                'type': 'json_object'
            }
        )
        rate_result = json.loads(structure_validation_response.choices[0].message.content)["metrics"]
        return rate_result
    def validate_structure(self, dialog_graph):
        structure = graph_to_JSON(self.validate_structure_alg(dialog_graph))
        return self.interpret_rate(self.validate_structure_llm(structure))
    def validate_content_llm(self, line, dialog_chains, character_stats, character):
        with open("resources/prompt_content_validation.txt", encoding = 'utf-8', mode= "r") as prompt_content_validation:
            prompt_content_validation = Template(prompt_content_validation.read()).safe_substitute(
            character = character,
            interlocutor = "игрок" if character == "NPC" else "NPC",
            dialog_chains = dialog_chains,
            line = line,
            name = character_stats["name"],
            talk_style = character_stats["talk_style"],
            profession = character_stats["profession"],
            look = character_stats["look"],
            relation = self.params["NPC_to_hero_relation"] if character == "NPC" else self.params["hero_to_NPC_relation"],
            traits = character_stats["traits"],
            character_extra = character_stats["extra"],
            genre = self.params["genre"],
            epoch = self.params["epoch"], 
            tonality = self.params["tonality"],
            world_settings = self.params["world_settings"],
            extra = self.params["extra"],
            json_metrics = self.llm_settings.get_json_metrics()
        )  
        validation_content_response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.llm_settings.get_system_prompt()},
                {"role": "user", "content": prompt_content_validation},
            ],
            stream=False,
            response_format={
                'type': 'json_object'
            }
        )
        rate_result = json.loads(validation_content_response.choices[0].message.content)["metrics"]
        return rate_result
    def prune_children(self, dialog_graph, node, used):
        if node not in used:
            used.append(node)
        for next_node in list(dialog_graph[node]):
            if next_node not in used:
                dialog_graph.nodes[next_node]["line"] = dialog_graph.edges[node, next_node]["line"] = ""
                dialog_graph.nodes[next_node]["validation_result"] = dialog_graph.edges[node, next_node]["validation_result"] = {} 
                self.prune_children(dialog_graph, next_node, used)
    def validate_node_line(self, dialog_graph, dialog_chain, node, used):
        result = self.interpret_rate(self.validate_content_llm(dialog_graph.nodes[node]["line"], dialog_chain, self.npc, "NPC"))
        dialog_graph.nodes[node]["validation_result"] = result[1]
        if not result[0]:
            dialog_graph.nodes[node]["line"] =  ""
            self.prune_children(dialog_graph, node, used)
        self.dialog_graph = dialog_graph
        return result[0]
    def validate_edge_line(self, dialog_graph, dialog_chain, edge, used):
        result = self.interpret_rate(self.validate_content_llm(dialog_graph.edges[edge]["line"], dialog_chain, self.hero, "главный герой"))
        # print(result)
        dialog_graph.edges[edge]["validation_result"] = result[1]
        if not result[0]:
            dialog_graph.edges[edge]["line"] = ""
            dialog_graph.nodes[edge[1]]["line"] =  ""
            self.prune_children(dialog_graph, edge[1], used)
        return result[0]
    def validate_content(self, dialog_graph):
        q = deque()
        start_node = list(dialog_graph.nodes)[0]
        q.append(start_node)
        used = []
        while q:
            t = q.popleft()
            used.append(t)
            prev_chains = []
            paths = list(nx.all_simple_paths(dialog_graph, source=start_node, target=t))
            next_nodes = list(dialog_graph.adj[t].keys())
            lst_node = -1
            for path in paths:
                dialog_chain = ""
                for ind in range(0, len(path)):
                    node = path[ind]
                    if ind < len(path)-1:
                        dialog_chain += f"**NPC**: {dialog_graph.nodes[node]["line"]}\n"
                    if ind:
                        dialog_chain += f"**Игрок**: {dialog_graph.edges[lst_node, node]["line"]}\n"
                    lst_node = node
                prev_chains.append(dialog_chain)
            if not self.validate_node_line(dialog_graph, prev_chains, t, used):
                continue
            for i in range(0, len(prev_chains)):
                prev_chains[i] += f"**NPC**: {dialog_graph.nodes[t]["line"]}\n"
            for next_node in next_nodes:
                # print((node, next_node), dialog_graph.edges[node, next_node]["line"])               
                if dialog_graph.edges[node, next_node]["line"] and self.validate_edge_line(dialog_graph, prev_chains, (node, next_node), used) and next_node not in used:
                    q.append(next_node)
        return dialog_graph
    
class DialogRegenerator(DialogSettings):
    def convert_metrcics(self, metrics):
        result = []
        for metric in metrics:
            result.append(f"{metric} ({metrics[metric]["rate"]}/10) - {metrics[metric]["comment"]}")
        return result

    def regenerate_structure(self, structure, metrics):
        with open("resources/prompt_structure_regeneration.txt", encoding='utf-8', mode="r") as prompt_structure:
            prompt_structure = Template(prompt_structure.read()).safe_substitute(
                json_structure=self.llm_settings.get_structure(),
                json_node_structure=self.llm_settings.get_node_structure(),
                NPC_name=self.npc["name"],
                NPC_talk_style=self.npc["talk_style"],
                NPC_profession=self.npc["profession"],
                NPC_look=self.npc["look"],
                NPC_traits=self.npc["traits"],
                NPC_extra=self.npc["extra"],
                hero_name=self.hero["name"],
                hero_talk_style=self.hero["talk_style"],
                hero_profession=self.hero["profession"],
                hero_look=self.hero["look"],
                hero_extra=self.hero["extra"],
                hero_traits=self.hero["traits"],
                NPC_to_hero_relation=self.params["NPC_to_hero_relation"],
                hero_to_NPC_relation=self.params["hero_to_NPC_relation"],
                world_settings=self.params["world_settings"],
                scene = self.params["scene"],
                genre = self.params["genre"],
                epoch = self.params["epoch"],
                tonality = self.params["tonality"],
                extra = self.params["extra"],
                context = self.params["context"],
                mx_answers_cnt=self.params["mx_answers_cnt"],
                mn_answers_cnt=self.params["mn_answers_cnt"],
                mx_depth=self.params["mx_depth"],
                mn_depth=self.params["mn_depth"],
                moods_list=self.llm_settings.get_moods(),
                goals=self.goals,
                structure = structure,
                comments = self.convert_metrics(metrics)
                )

        structure_response = self.client.chat.completions.create(
            model=self.dialogue_model_type,
            messages=[
                {"role": "system", "content": self.llm_settings.get_system_prompt()},
                {"role": "user", "content": prompt_structure},
            ],
            stream=False,
            max_tokens=self.structure_model_max_tokens,
            temperature=0.6,
            top_p=0.95,
            response_format={
                'type': 'json_object'
            }
        )

        structure = json.loads(structure_response.choices[0].message.content)
        return structure
    
    def regenerate_content(self, dialog_validator, dialog_graph):
        q = deque()
        start_node = list(dialog_graph.nodes)[0]
        q.append(start_node)
        used = []
        while q:
            t = q.popleft()
            used.append(t)
            next_required_replics = []
            next_required_nodes = []
            prev_chains = []
            paths = list(nx.all_simple_paths(dialog_graph, source=start_node, target=t))
            next_nodes = list(dialog_graph.adj[t].keys())
            lst_node = -1
            for path in paths:
                dialog_chain = ""
                for ind in range(0, len(path)):
                    node = path[ind]
                    if ind < len(path)-1 and dialog_graph.nodes[node].get("line"):
                        dialog_chain += f"**NPC**: {dialog_graph.nodes[node]["line"]}\n"
                    if ind and dialog_graph.edges[lst_node, node].get("line"):
                        dialog_chain += f"**Игрок**: {dialog_graph.edges[lst_node, node]["line"]}\n"
                    lst_node = node
                prev_chains.append(dialog_chain)
            
            for next_node in next_nodes:
                if not dialog_graph.edges[node, next_node].get("line"):
                    next_required_replics.append(dialog_graph.nodes[next_node]["info"])
                    next_required_nodes.append(next_node)
                if next_node not in q and next_node not in used:
                    q.append(next_node)
            validation_result = dialog_graph.nodes[t].get("line")
            while not validation_result:
                with open("resources/prompt_nodes_content.txt", encoding='utf-8', mode="r") as prompt_nodes_content:
                    prompt_nodes_content = Template(prompt_nodes_content.read()).safe_substitute(
                    chain="\n = = = = \n".join(prev_chains),
                    tematic=dialog_graph.nodes[t]["info"],
                    world_settings=self.params["world_settings"],
                    name=self.npc["name"],
                    talk_style=self.npc["talk_style"],
                    profession=self.npc["profession"],
                    traits=self.npc["traits"],
                    scene=self.params["scene"],
                    extra=self.params["extra"],
                    look=self.npc["look"],
                    mood=dialog_graph.nodes[t]["mood"],
                    relation=self.params["NPC_to_hero_relation"]
                )
                node_content_response = self.client.chat.completions.create(
                    model=self.dialogue_model_type,
                    messages=[
                        {"role": "system", "content": self.llm_settings.get_system_prompt()},
                        {"role": "user", "content": prompt_nodes_content},
                    ],
                    stream=False,
                    max_tokens=self.structure_model_max_tokens
                )
                dialog_graph.nodes[t]["line"] = node_content_response.choices[0].message.content.strip("\"\'")
                validation_result = dialog_validator.validate_node_line(dialog_graph, prev_chains, t, copy.deepcopy(list(dialog_graph.adj[t])))
            for i in range(0, len(prev_chains)):
                prev_chains[i] += f"**NPC**: {dialog_graph.nodes[t]["line"]}\n"
            while len(next_required_replics):
                with open("resources/prompt_edges_content.txt", encoding='utf-8', mode="r") as prompt:
                    prompt_edges_content = Template(prompt.read()).safe_substitute(
                    json_edge_structure=self.llm_settings.get_edge_structure(),
                    chain="\n = = = = \n".join(prev_chains),
                    tematics="\n = = = = \n".join(next_required_replics),
                    replic_cnt=len(next_required_replics),
                    world_settings=self.params["world_settings"],
                    name=self.hero["name"],
                    talk_style=self.hero["talk_style"],
                    profession=self.hero["profession"],
                    traits=self.hero["traits"],
                    look=self.hero["look"],
                    hero_extra=self.hero["extra"],
                    mood=dialog_graph.nodes[t]["mood"],
                    extra=self.params["extra"],
                    scene=self.params["scene"],
                    relation=self.params["hero_to_NPC_relation"]
                )
                edge_content_response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": self.llm_settings.get_system_prompt()},
                        {"role": "user", "content": prompt_edges_content},
                    ],
                    stream=False,
                    response_format={
                        'type': 'json_object'
                    }
                )
                edges_meta = json.loads(edge_content_response.choices[0].message.content)["lines"]
                next_required_replics_new = []
                next_required_nodes_new = []
                for i in range(0, len(next_required_replics)):
                    if dialog_validator.validate_edge_line(dialog_graph, dialog_chain, (t, next_required_nodes[i]), copy.deepcopy(list(dialog_graph.adj[t]))):
                        for key in edges_meta[i].keys():
                            dialog_graph.edges[t, next_required_nodes[i]][key] = edges_meta[i][key].strip("\"\'")
                    else:
                        next_required_replics_new.append(next_required_replics[i])
                        next_required_nodes_new.append(next_required_nodes[i])
                next_required_replics = next_required_replics_new
                next_required_nodes = next_required_nodes_new
        return dialog_graph
