import logging
import os

# Путь до лог-файла
log_dir = "logs"
log_file = os.path.join(log_dir, "db.log")

# Убедимся, что директория существует
os.makedirs(log_dir, exist_ok=True)

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_file,
    filemode="a"
)


logger = logging.getLogger("screenwriter")
