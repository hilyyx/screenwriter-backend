import os


def load_prompt(filename: str) -> str:
    """
    Загружает шаблон из файла prompt.txt из папки resources.
    Ищет сначала относительно текущего файла, затем от корня проекта.
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Путь: ../resources/filename
    candidate_paths = [
        os.path.join(current_dir, '..', 'resources', filename),  # путь относительно lib
        os.path.join(current_dir, '..', '..', 'resources', filename),  # путь относительно lib/llm и т.д.
        os.path.join(os.path.abspath(os.curdir), 'resources', filename),  # путь от запуска
    ]

    for path in candidate_paths:
        full_path = os.path.abspath(path)
        if os.path.isfile(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()

    raise FileNotFoundError(f"Не удалось найти файл '{filename}' в папке 'resources'. Проверенные пути:\n" +
                            "\n".join(os.path.abspath(p) for p in candidate_paths))
