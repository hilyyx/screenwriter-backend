from string import Template
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from resources.loaders import load_prompt
from lib.llm.settings import (json_structure, json_node_structure_meta, json_structure_meta, character_stats_structure,
                              world_settings, goals, NPC_settings, hero_settings)


def generate_dialogue_from_params(params: dict) -> list:
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    prompt1 = load_prompt("prompt.txt")

    npc = params["npc"]
    hero = params["hero"]
    goals = params["goals"]
    goals_for_prompt = [
        {"Тип": "Получение предмета", "Объект": "Ключ-карта от секретного хранилища", "Условие": "Предоставить исторические данные"}
    ]

    with open("resources/prompt.txt", encoding='utf-8', mode="r") as prompt:
        prompt = Template(prompt.read()).safe_substitute(
            json_structure=json_structure_meta,
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
            NPC_to_hero_relation="Не знаком",
            hero_to_NPC_relation="Не знаком",
            world_settings=params["world_settings"],
            json_node_structure=json_node_structure_meta,
            mx_answers_cnt=5,
            mn_answers_cnt=2,
            mx_plot_branches_cnt=5,
            mx_depth=15,
            mn_depth=15,
            goals=goals_for_prompt)
    print(prompt)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": """Ты главный сценарист крупнейшей в России студии по разработке видеоигр.\n    Ты прописываешь диалоги главного героя и NPC для игры, в которую будут играть школьники.\n    Ты **обязан** следить, чтобы диалоги могли читать дети. Ты **обязан избегать ругательств**"""},
            {"role": "user", "content": prompt1},
        ],
        stream=False,
        max_tokens=20000,
        temperature=0.6,
        top_p=0.95,
        response_format={
            'type': 'json_object'
        }
    )

    parsed = json.loads(response.choices[0].message.content)
    return parsed
