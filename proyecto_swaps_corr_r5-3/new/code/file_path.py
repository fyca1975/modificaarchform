# code/file_path.py
from __future__ import annotations
from pathlib import Path
from typing import Dict
import os
from dotenv import load_dotenv
from logger import get_logger


# === Añadido: validador de variables .env que deben ser rutas ===
import os as _os, re as _re
try:
    from logger import get_logger as _get_logger  # usa tu logger si está disponible
    _log = _get_logger(__name__)
except Exception:  # fallback mínimo
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)
    _log = _logging.getLogger(__name__)

def get_env(key: str) -> str:
    """
    Obtiene el valor de una variable de entorno desde .env y valida que parezca ruta de directorio.
    - Soporta Windows y Unix-like.
    - Lanza ValueError si no cumple el patrón de ruta esperado.

    Args:
        key: Nombre de la variable de entorno a leer (p.ej. "INPUT_DIR")

    Returns:
        str: Ruta tal como viene del .env (no normaliza separadores).

    Raises:
        ValueError: Si la variable no existe o no cumple validaciones básicas de ruta.
    """
    try:
        folder_path = _os.getenv(key)

        if not folder_path:
            raise ValueError(f"No se encontró la variable de entorno: {key}")

        # Validación general (Windows + Unix). No impone existencia, solo formato.
        regex1 = r"^[A-Za-z]:\\(?:[^<>:\"/\\|?*\n]+\\?)*[^<>:\"/\\|?*\n]*$"   # Windows (C:\...)
        regex2 = r"^[A-Za-z0-9_\[\]\"`'.,\s\\/\-<>@{}:+]+$"                  # Unix/otros (permite /)

        if not _re.match(regex1, folder_path):
            if not _re.match(regex2, folder_path):
                raise ValueError(f"El valor de la llave '{key}' no es una ruta válida (formato).")

    except ValueError as e:
        _log.error(f'Error: {e}')
        raise
    except Exception as e:
        _log.error(f'Error obteniendo variable {key}: {e}')
        raise

    return folder_path
# === Fin añadido get_env ===
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

log = get_logger(__name__)

def _abs_from_code_root(path_str: str) -> Path:
    base = Path(__file__).resolve().parents[1]
    if path_str.startswith("../"):
        return (base / "code" / path_str).resolve()
    return (base / path_str).resolve() if not Path(path_str).is_absolute() else Path(path_str).resolve()

def ensure_dir(path: Path, key: str, create: bool) -> Path:
    if create:
        path.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        raise FileNotFoundError(f"La ruta para {key} no existe: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"La ruta para {key} no es un directorio: {path}")
    return path

def load_paths() -> Dict[str, str]:
    input_dir = os.getenv("INPUT_DIR", "../input")
    output_dir = os.getenv("OUTPUT_DIR", "../output")
    log_dir = os.getenv("LOG_DIR", "../logs")

    p_input = ensure_dir(_abs_from_code_root(input_dir), "INPUT_DIR", create=False)
    p_output = ensure_dir(_abs_from_code_root(output_dir), "OUTPUT_DIR", create=True)
    p_log = ensure_dir(_abs_from_code_root(log_dir), "LOG_DIR", create=True)

    rutas = {
        "INPUT_DIR": str(p_input),
        "OUTPUT_DIR": str(p_output),
        "LOG_DIR": str(p_log),
    }
    log.info(f"Rutas normalizadas: {rutas}")
    return rutas
