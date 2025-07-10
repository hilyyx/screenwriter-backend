from string import Template
from networkx import DiGraph
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque

from lib.llm.settings import json_node_structure, json_structure, system_prompt

import networkx as nx
import os
import json


def generate_dialogue_from_params(params: dict):
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    model_type = os.getenv("MODEL_TYPE")

    npc = params["npc"]
    hero = params["hero"]
    goals = params["goals"]
    goals_for_prompt = [
        {"Тип": "Получение предмета", "Объект": "Ключ-карта от секретного хранилища", "Условие": "Предоставить исторические данные"}
    ]

    with open("resources/prompt.txt", encoding='utf-8', mode="r") as prompt:
        prompt = Template(prompt.read()).safe_substitute(
            json_structure=json_structure,
            NPC_name=npc["name"],
            NPC_goal=npc["goal"],
            NPC_talk_style=npc["talk_style"],
            NPC_profession=npc["profession"],
            NPC_traits=npc["traits"],
            hero_name=hero["name"],
            hero_goal=hero["goal"],
            hero_talk_style=hero["talk_style"],
            hero_profession=hero["profession"],
            hero_traits=hero["traits"],
            NPC_to_hero_relation=params["NPC_to_hero_relation"],
            hero_to_NPC_relation=params["hero_to_NPC_relation"],
            world_settings=params["world_settings"],
            json_node_structure=json_node_structure,
            mx_answers_cnt=5,
            mn_answers_cnt=2,
            mx_plot_branches_cnt=5,
            mx_depth=15,
            mn_depth=15,
            goals=goals_for_prompt)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model=model_type,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        #max_tokens=20000,
        temperature=0.6,
        top_p=0.95,
        response_format={
            'type': 'json_object'
        }
    )

    parsed = json.loads(response.choices[0].message.content)

    dialog_graph = nx.DiGraph()
    for node in parsed['data']:
        dialog_graph.add_node(
            node["id"],
            tematic=node["info"]
        )
        for child in node['to']:
            dialog_graph.add_edge(node["id"], child["id"])
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
                    dialog_chain += f'**NPC**: {dialog_graph.nodes[node]["tematic"]}\n'
                if ind:
                    dialog_chain += f'**Игрок**: {dialog_graph.edges[lst_node, node]["replic"]}\n'
                lst_node = node
            prev_chains.append(dialog_chain)
        for next_node in next_nodes:
            next_replics.append(dialog_graph.nodes[next_node]["tematic"])
            if next_node not in q:
                q.append(next_node)
        with open("resources/prompt_nodes_content.txt", encoding='utf-8', mode="r") as prompt:
            prompt_nodes_content = Template(prompt.read()).safe_substitute(
                chain="\n = = = = \n".join(prev_chains),
                tematic=dialog_graph.nodes[t]["tematic"],
                world_settings=params["world_settings"],
                name=npc["name"],
                talk_style=npc["talk_style"],
                profession=npc["profession"],
                traits=npc["traits"],
                relation=params["NPC_to_hero_relation"]
            )
        response = client.chat.completions.create(
            model=model_type,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_nodes_content},
            ],
            stream=False
        )
        dialog_graph.nodes[t]["replic"] = response.choices[0].message.content
        for i in range(0, len(prev_chains)):
            prev_chains[i] += f'**NPC**: {dialog_graph.nodes[t]["replic"]}\n'
        with open("resources/prompt_edges_content.txt", encoding='utf-8', mode="r") as prompt:
            prompt_edges_content = Template(prompt.read()).safe_substitute(
                chain="\n = = = = \n".join(prev_chains),
                tematics="\n = = = = \n".join(next_replics),
                replic_cnt=len(next_replics),
                world_settings=params["world_settings"],
                name=hero["name"],
                talk_style=hero["talk_style"],
                profession=hero["profession"],
                traits=hero["traits"],
                relation=params["hero_to_NPC_relation"]
            )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_edges_content},
            ],
            stream=False,
            response_format={
                'type': 'json_object'
            }
        )
        answers = json.loads(response.choices[0].message.content)["replics"]
        for i in range(0, len(next_replics)):
            dialog_graph.edges[t, next_nodes[i]]["replic"] = answers[i]

    graph = {"data": []}
    for node in list(dialog_graph.nodes):
        graph["data"].append(dialog_graph.nodes[node])
        graph["data"][-1]["id"] = node
        graph["data"][-1]["to"] = []
        for next_node in list(dialog_graph.adj[node].keys()):
            graph["data"][-1]["to"].append(dialog_graph.edges[(node, next_node)])
            graph["data"][-1]["to"][-1]["id"] = next_node

    return graph


