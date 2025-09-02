import re
import os
from logger import log  # Asegúrate de que este módulo exista y tenga un método log.error

def get_env(key):
    """
    Función que obtiene el valor de una variable de entorno desde un archivo .env
    y valida que sea una ruta de directorio válida.

    Args:
        key (str): Nombre de la variable de entorno

    Returns:
        str: Ruta del directorio

    Raises:
        ValueError: Si el valor de la variable no tiene un formato válido
    """
    try:
        folder_path = os.getenv(key)

        if not folder_path:
            raise ValueError(f"No se encontró la variable de entorno: {key}")

        # Validación general (Windows + Unix)
        regex1 = r"^[A-Za-z0-9]:\\(?:[^<>:\"/\\|?*\n]+\\?)*[^<>:\"/\\|?*\n]*$"  # Windows
        regex2 = r"^[A-Za-z0-9_\[\]\"`'.,\s\\\-<>@{}:+]+$"                    # Unix/otros

        if not re.match(regex1, folder_path):
            if not re.match(regex2, folder_path):
                raise ValueError(f"El valor de la llave '{key}' no es una ruta válida.")

    except ValueError as e:
        log.error(f'Error: {e}')
    except Exception as e:
        log.error(f'Error obteniendo variable {key}: {e}')

    return folder_path
