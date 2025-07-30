import os
import logging

def cargar_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    rutas = {}
    with open(env_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                rutas[key.strip()] = value.strip().replace('"', '').replace("'", "")
    return rutas

def setup_logging(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "swaps.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
