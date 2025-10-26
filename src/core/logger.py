import logging
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("Frontend API")
logger.setLevel("INFO")
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setLevel("INFO")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
