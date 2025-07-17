class LLMSettings:
    json_node_structure = '''
    {
        "id": "*Уникальный числовой идентификатор для текущей вершины*", 
        "info": "*Краткое описание контекста и тематики монолога NPC*",
        "type": "*Тип вершины*", 
        "mood": "*Настроение NPC в данной вершине*",
        "goal_achieve": "*Достиг ли герой цели в данной вершине*",
        "to":
        [
            {
                "id": "*id вершины в которую идёт ребро диалога из данной вершины*",
                "mood": "*Настроение главного героя в данном ребре*"
            },
            ...
        ]
    }
    '''

    json_structure = f'''
        {{
            "data": 
            [
                {{
                    {json_node_structure}
                }},
            ]
        }}
        '''
    json_edge_structure = '''
    {
        "lines": 
        [
            {
                "line": "*реплика*",
                "info": "*краткое описание реплики*"
            },
            ...
        ]
    }

    '''
    json_metrics = '''
    {
        "metrics": 
        {
            "*Название проверки 1*": {
                "rate": *Численное значение оценки для проверки 1*,
                "comment": "*Комментарий о том, что не соответствует проверке 1 в структуре графа. Если всё хорошо, оставь это поле пустым*"
            },
            ...
        }
    }
    '''
    moods = ["радостный", "благодарный", "воодушевлёный", "нейтральный", "растерянный", "грустный", "испуганный", "злой"]
    system_prompt = """Ты главный сценарист крупнейшей в России студии по разработке видеоигр.\n\n    Ты прописываешь диалоги главного героя и NPC для игры, в которую будут играть школьники.\n\n        Ты **обязан** следить, чтобы диалоги могли читать дети. Ты **обязан избегать ругательств**"""
    
    @classmethod
    def get_node_structure(cls):
        return cls.json_node_structure

    @classmethod
    def get_structure(cls):
        return cls.json_structure

    @classmethod
    def get_edge_structure(cls):
        return cls.json_edge_structure

    @classmethod
    def get_moods(cls):
        return cls.moods

    @classmethod
    def get_system_prompt(cls):
        return cls.system_prompt
    
    @classmethod
    def get_json_metrics(cls):
        return cls.json_metrics
