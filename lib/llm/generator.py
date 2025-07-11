from string import Template
from networkx import DiGraph
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque

from lib.llm.settings import LLMSettings

import networkx as nx
import os
import json


class DialogGenerator:
    def __init__(self, params: dict):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model_type = os.getenv("MODEL_TYPE")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

        self.params = params
        self.npc = self.params["npc"]
        self.hero = self.params["npc"]
        self.goals = self.params["goals"]
        self.llm_settings = LLMSettings()

    def generate_structure(self):

        goals_for_prompt = [{"Тип": "Получение предмета", "Объект": "Ключ-карта от секретного хранилища",
                             "Условие": "Предоставить исторические данные"}]

        with open("resources/prompt_structure.txt", encoding='utf-8', mode="r") as prompt_structure:
            prompt_structure = Template(prompt_structure.read()).safe_substitute(
                json_structure=self.llm_settings.get_structure(),
                NPC_name=self.npc["name"],
                NPC_goal=self.npc["goal"],
                NPC_talk_style=self.npc["talk_style"],
                NPC_profession=self.npc["profession"],
                NPC_traits=self.npc["traits"],
                hero_name=self.hero["name"],
                hero_goal=self.hero["goal"],
                hero_talk_style=self.hero["talk_style"],
                hero_profession=self.hero["profession"],
                hero_traits=self.hero["traits"],
                NPC_to_hero_relation=self.params["NPC_to_hero_relation"],
                hero_to_NPC_relation=self.params["hero_to_NPC_relation"],
                world_settings=self.params["world_settings"],
                json_node_structure=self.llm_settings.get_node_structure(),
                mx_answers_cnt=5,
                mn_answers_cnt=2,
                mx_plot_branches_cnt=5,
                mx_depth=15,
                mn_depth=15,
                goals=goals_for_prompt)

        structure_response = self.client.chat.completions.create(
            model=self.model_type,
            messages=[
                {"role": "system", "content": self.llm_settings.get_system_prompt()},
                {"role": "user", "content": prompt_structure},
            ],
            stream=False,
            # max_tokens=20000,
            temperature=0.6,
            top_p=0.95,
            response_format={
                'type': 'json_object'
            }
        )

        parsed = json.loads(structure_response.choices[0].message.content)

        dialog_graph = nx.DiGraph()
        for node in parsed['data']:
            dialog_graph.add_node(
                node["id"],
                info=node["info"]
            )
            for child in node['to']:
                dialog_graph.add_edge(node["id"], child["id"])
        return dialog_graph
    def generate_dialogue(self, dialog_graph):
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
                    relation=self.params["NPC_to_hero_relation"]
                )
            response = self.client.chat.completions.create(
                model=self.model_type,
                messages=[
                    {"role": "system", "content": self.llm_settings.get_system_prompt()},
                    {"role": "user", "content": prompt_nodes_content},
                ],
                stream=False
            )
            dialog_graph.nodes[t]["line"] = response.choices[0].message.content
            for i in range(0, len(prev_chains)):
                prev_chains[i] += f'**NPC**: {dialog_graph.nodes[t]["line"]}\n'
            with open("resources/prompt_edges_content.txt", encoding='utf-8', mode="r") as prompt:
                prompt_edges_content = Template(prompt.read()).safe_substitute(
                    chain="\n = = = = \n".join(prev_chains),
                    tematics="\n = = = = \n".join(next_replics),
                    replic_cnt=len(next_replics),
                    world_settings=self.params["world_settings"],
                    name=self.hero["name"],
                    talk_style=self.hero["talk_style"],
                    profession=self.hero["profession"],
                    traits=self.hero["traits"],
                    relation=self.params["hero_to_NPC_relation"]
                )
            response = self.client.chat.completions.create(
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
            answers = json.loads(response.choices[0].message.content)["lines"]
            for i in range(0, len(next_replics)):
                dialog_graph.edges[t, next_nodes[i]]["line"] = answers[i]

        graph = {"data": []}
        for node in list(dialog_graph.nodes):
            graph["data"].append(dialog_graph.nodes[node])
            graph["data"][-1]["id"] = node
            graph["data"][-1]["to"] = []
            for next_node in list(dialog_graph.adj[node].keys()):
                graph["data"][-1]["to"].append(dialog_graph.edges[(node, next_node)])
                graph["data"][-1]["to"][-1]["id"] = next_node

        return graph

