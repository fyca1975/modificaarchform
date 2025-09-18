from __future__ import annotations

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

# Import after __future__
from file_path import load_paths


def cargar_env() -> dict:
    """
    Carga variables desde .env, normaliza rutas con file_path.load_paths()
    y devuelve un diccionario unificado con configuración.
    """
    # Intentar cargar .env junto a la carpeta 'code' (un nivel arriba de pkg/)
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Fallback a cualquier .env en el CWD
        load_dotenv()

    # Normalizar rutas base desde file_path (INPUT_DIR, OUTPUT_DIR, LOG_DIR)
    rutas = load_paths()

    # Variables de logging (permiten override desde .env)
    log_dir = os.getenv("LOG_DIR", rutas.get("LOG_DIR", "logs"))
    log_file = os.getenv("LOG_FILE", "app.log")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    max_bytes = int(os.getenv("LOG_MAX_BYTES", "1048576"))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # Merge y normalización
    rutas.update({
        "LOG_DIR": str(Path(log_dir)),
        "LOG_FILE": log_file,
        "LOG_LEVEL": log_level,
        "LOG_MAX_BYTES": max_bytes,
        "LOG_BACKUP_COUNT": backup_count,
    })
    return rutas


def setup_logging(
    log_dir: str,
    log_file: str = "app.log",
    level: str = "INFO",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
) -> logging.Logger:
    """Configura un logger rotativo a archivo + consola."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Logger raíz
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level, logging.INFO))

    # Evitar handlers duplicados al reconfigurar
    for h in list(logger.handlers):
        logger.removeHandler(h)

    log_path = Path(log_dir) / log_file

    file_handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Mensajes de diagnóstico (visibles en tu salida)
    logging.getLogger("file_path").info("Logger configurado")
    logging.getLogger("file_path").info(
        "LOG_DIR=%s | LOG_FILE=%s | LEVEL=%s | MAX_BYTES=%s | BACKUP_COUNT=%s",
        log_dir, log_file, level, max_bytes, backup_count
    )
    return logger
