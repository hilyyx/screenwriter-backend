import os

def load_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base_dir, "resources", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
