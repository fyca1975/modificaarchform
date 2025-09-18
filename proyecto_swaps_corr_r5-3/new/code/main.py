from __future__ import annotations

import logging

# Imports del proyecto
from pkg.utils import cargar_env, setup_logging
from pkg.procesar_swaps import procesar_swaps  # Asegúrate de que exista
from pkg.actualizar_informe import actualizar_informe  # Asegúrate de que exista


def main() -> None:
    # 1) Cargar variables y rutas centralizadas
    rutas = cargar_env()

    # 2) Configurar logging una vez con los valores finales
    setup_logging(
        rutas["LOG_DIR"],
        rutas.get("LOG_FILE", "app.log"),
        rutas.get("LOG_LEVEL", "INFO"),
        rutas.get("LOG_MAX_BYTES", 1_048_576),
        rutas.get("LOG_BACKUP_COUNT", 5),
    )

    log = logging.getLogger(__name__)
    log.info("Inicializando proceso con rutas: %s", rutas)

    # 3) Lógica de negocio con manejo de errores explícito
    try:
        ok_swaps = procesar_swaps(rutas["INPUT_DIR"], rutas["OUTPUT_DIR"])
    except Exception:
        log.exception("Fallo en procesar_swaps")
        raise

    if ok_swaps:
        try:
            actualizado = actualizar_informe(rutas["OUTPUT_DIR"])
        except Exception:
            log.exception("Fallo en actualizar_informe")
            raise

        if actualizado:
            log.info("Proceso completado y archivos generados exitosamente.")
        else:
            log.warning("Archivo de informe R5 no encontrado. Proceso finalizado solo con swaps.")
    else:
        log.error("Error al procesar el archivo de flujos de swaps.")

    log.info("----- FIN DEL PROCESO -----")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Error no controlado en main()")
        raise
