# code/pkg/utils.py
from __future__ import annotations
from pathlib import Path
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Carga central del .env (idempotente)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"  # /code/.env
load_dotenv(ENV_PATH)

def cargar_env() -> dict:
    """Devuelve las rutas y variables base desde .env (con valores por defecto).
    Normaliza las rutas relativas ../ respecto a /code en file_path.load_paths()."""
    rutas = {
        "INPUT_DIR": os.getenv("INPUT_DIR", "../input"),
        "OUTPUT_DIR": os.getenv("OUTPUT_DIR", "../output"),
        "LOG_DIR": os.getenv("LOG_DIR", "../logs"),
    }
    # No normalizamos aquí; lo hace file_path.load_paths()
    return rutas

def setup_logging(log_dir: str | None = None):
    """Compat: configura logging usando variables del .env.
    Si no se pasa log_dir, usa LOG_DIR del .env.
    """
    from logger import get_logger  # evita dependencia circular
    # Instancia el logger raíz para configurar handlers según .env
    root_logger = get_logger()  # aplica rotación y consola
    if log_dir:
        # Asegura que exista (por si se invoca con ruta específica)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    return root_logger

def get_config(key: str, default=None):
    return os.getenv(key, default)
