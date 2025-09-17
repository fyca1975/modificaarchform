# -*- coding: utf-8 -*-
"""
Logger centralizado con resolución robusta de rutas (Punto 3).
- Lee variables desde .env con defaults seguros (no rompe lógica actual).
- Resuelve LOG_DIR relativo a la raíz del repo (basado en ubicación de este archivo).
- Evita duplicar handlers si se llama varias veces.
"""

from __future__ import annotations
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # si no está instalada, el logger funcionará con defaults
    load_dotenv = None  # type: ignore

# --- Localiza la raíz del proyecto y el archivo .env ---
_CODE_DIR = Path(__file__).resolve().parent
# Asumimos estructura repo/<raiz>/code/logger.py  -> raíz = parents[1]
_REPO_ROOT = _CODE_DIR.parents[1] if len(_CODE_DIR.parents) >= 2 else _CODE_DIR

def _load_dotenv_if_available() -> None:
    """Carga .env si python-dotenv está disponible. Prioriza .env en /code o en la raíz."""
    if load_dotenv is None:
        return
    # Candidatos: code/.env y .env en la raíz del repo
    candidates = [
        _CODE_DIR / ".env",
        _REPO_ROOT / ".env",
        _CODE_DIR / ".env.local",
        _REPO_ROOT / ".env.local",
    ]
    for p in candidates:
        if p.exists():
            load_dotenv(dotenv_path=p, override=False)  # no pisa variables ya cargadas
            break

# Ejecuta la carga .env una sola vez
_load_dotenv_if_available()

# --- Lee variables de entorno con defaults seguros ---
_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
_LOG_DIR = os.getenv("LOG_DIR", "../logs")
_LOG_FILE = os.getenv("LOG_FILE", "app.log")
_LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "1048576"))  # 1 MiB
_LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
_LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
_LOG_DATEFMT = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")

# --- Resuelve LOG_DIR relativo a la raíz del repo (punto 3) ---
def _resolve_log_dir(raw_log_dir: str) -> Path:
    # Si es una ruta absoluta, úsala directamente
    p = Path(raw_log_dir)
    if p.is_absolute():
        return p

    # Si empieza con ../ asumimos que se quiere relativo a code/
    if raw_log_dir.startswith("../"):
        base = _CODE_DIR  # desde code/
        resolved = (base / raw_log_dir).resolve()
        return resolved

    # En otro caso, lo resolvemos respecto a la raíz del repo
    resolved = (_REPO_ROOT / raw_log_dir).resolve()
    return resolved

_LOG_DIR_PATH = _resolve_log_dir(_LOG_DIR)
_LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)
_LOG_PATH = (_LOG_DIR_PATH / _LOG_FILE).resolve()

# Guardamos estado para no duplicar handlers
_CONFIGURED_LOGGERS = set()

def get_logger(name: str | None = None) -> logging.Logger:
    """
    Devuelve un logger configurado con RotatingFileHandler y StreamHandler.
    Evita duplicar handlers si se invoca múltiples veces.
    """
    logger = logging.getLogger(name if name else "app")
    if logger.name in _CONFIGURED_LOGGERS:
        return logger

    # Nivel
    level = getattr(logging, _LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    # Formato
    formatter = logging.Formatter(fmt=_LOG_FORMAT, datefmt=_LOG_DATEFMT)

    # Handler archivo rotativo
    file_handler = RotatingFileHandler(
        filename=str(_LOG_PATH),
        maxBytes=_LOG_MAX_BYTES,
        backupCount=_LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Handler consola
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Marca como configurado
    _CONFIGURED_LOGGERS.add(logger.name)

    # Log inicial de configuración (solo una vez por logger)
    logger.info("Logger configurado")
    logger.info("LOG_DIR=%s | LOG_FILE=%s | LEVEL=%s | MAX_BYTES=%s | BACKUP_COUNT=%s",
                str(_LOG_DIR_PATH), _LOG_FILE, _LOG_LEVEL, _LOG_MAX_BYTES, _LOG_BACKUP_COUNT)
    return logger
