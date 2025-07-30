# Proyecto Swaps - Automatización de Procesamiento de Archivos

## Objetivo

Automatizar el procesamiento y actualización de archivos de flujos de swaps usando archivos planos y reglas de negocio, asegurando calidad, trazabilidad y extensión.

## Estructura

proyecto_swaps/
├── input/          # Archivos de entrada (.csv, .dat)
├── output/         # Archivos generados
├── logs/           # Logs de ejecución
├── code/
│   ├── main.py
│   ├── .env
│   └── pkg/
│       ├── procesar_swaps.py
│       ├── actualizar_informe.py
│       └── utils.py

## Requisitos

- Python 3.8+
- pandas

Instala dependencias:
```bash
pip install pandas
```

## Ejecución

```bash
cd code
python main.py
```

## Ejemplo Archivos de Entrada

- `input/flujos_swap_gbo_20250603.csv`
- `input/COL_ESTIM_FLOWS_03062025.dat`
- `input/Informe_R5_GBO_250603.csv`
