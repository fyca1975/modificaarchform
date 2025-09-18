from __future__ import annotations

import logging
from pathlib import Path
from datetime import date

# Imports del proyecto
from pkg.utils import cargar_env, setup_logging
from pkg.procesar_swaps import procesar_swaps  # Debe devolver dict: {'ok': bool, 'flujos_csv': str, 'fecha': str}
from pkg.actualizar_informe import actualizar_informe  # Firma: actualizar_informe(output_dir, flujos_csv, fecha)


def _fallback_fecha() -> str:
    """Fecha fallback en formato ISO (YYYY-MM-DD)."""
    return date.today().isoformat()


def _validar_resultado_swaps(res: dict, output_dir: str) -> tuple[str, str]:
    """Valida el contrato de salida de procesar_swaps.
    Retorna (flujos_csv, fecha). Lanza ValueError si falta algo esencial.
    """
    if not isinstance(res, dict) or not res.get("ok"):
        raise ValueError("procesar_swaps no retornó ok=True")

    flujos_csv = res.get("flujos_csv")
    fecha = res.get("fecha")

    if not flujos_csv:
        # Intento de ruta por defecto
        candidato = Path(output_dir) / "flujos_procesados.csv"
        if candidato.exists():
            flujos_csv = str(candidato)
        else:
            raise ValueError("procesar_swaps no entregó 'flujos_csv' y no se encontró el archivo por defecto")

    if not fecha:
        fecha = _fallback_fecha()

    return str(flujos_csv), str(fecha)


def main() -> None:
    # 1) Cargar variables y rutas centralizadas (.env + file_path)
    rutas = cargar_env()

    # 2) Configurar logging con valores finales
    setup_logging(
        rutas["LOG_DIR"],
        rutas.get("LOG_FILE", "app.log"),
        rutas.get("LOG_LEVEL", "INFO"),
        rutas.get("LOG_MAX_BYTES", 1_048_576),
        rutas.get("LOG_BACKUP_COUNT", 5),
    )

    log = logging.getLogger(__name__)
    log.info("Inicializando proceso con rutas: %s", rutas)

    # 3) Procesar flujos
    try:
        res = procesar_swaps(rutas["INPUT_DIR"], rutas["OUTPUT_DIR"])
    except Exception:
        log.exception("Fallo en procesar_swaps")
        raise

    try:
        flujos_csv, fecha = _validar_resultado_swaps(res, rutas["OUTPUT_DIR"])
    except Exception as e:
        log.error("Resultado inválido de procesar_swaps: %s", e)
        return

    # 4) Actualizar informe con los argumentos requeridos
    try:
        actualizado = actualizar_informe(
            output_dir=rutas["OUTPUT_DIR"],
            flujos_csv=flujos_csv,
            fecha=fecha,
        )
    except Exception:
        log.exception("Fallo en actualizar_informe")
        raise

    if actualizado:
        log.info("Proceso completado y archivos generados exitosamente.")
    else:
        log.warning("Informe no actualizado (verifique insumos y plantillas).")

    log.info("----- FIN DEL PROCESO -----")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Error no controlado en main()")
        raise
