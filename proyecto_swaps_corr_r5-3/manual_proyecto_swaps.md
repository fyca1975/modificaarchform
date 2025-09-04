# Manual Técnico y de Uso

## Proyecto: Automatización de Procesamiento de Archivos de Swaps

---

## 1. Resumen y Objetivo

Este proyecto tiene como objetivo **automatizar el procesamiento y actualización de archivos de flujos de swaps**, integrando datos provenientes de archivos planos (.csv y .dat), aplicando reglas de negocio para asegurar la calidad y trazabilidad de los resultados. El flujo completo abarca desde la lectura, transformación, actualización y escritura de los archivos finales, junto con el registro detallado del proceso.

---

## 2. Estructura del Proyecto

```
proyecto_swaps_corr_r5/
│
├── README.md
├── .gitignore
├── input/           # Archivos de entrada (.csv, .dat)
├── output/          # Archivos de salida procesados
├── logs/            # Registro de ejecución
├── code/
│   ├── main.py      # Script principal de ejecución
│   ├── .env
│   └── pkg/         # Módulos de procesamiento
│        ├── procesar_swaps.py
│        ├── utils.py
│        └── actualizar_informe.py
└── .git/            # Control de versiones
```

- **input/**: Aquí se ubican los archivos a procesar (flujos de swaps, informes, estimaciones).
- **output/**: Aquí se generan los archivos finales ya procesados.
- **logs/**: Registro detallado del proceso, errores y trazabilidad.
- **code/**: Código fuente principal y módulos auxiliares.
- **.env, .gitignore**: Buenas prácticas para mantener el entorno limpio y seguro.

---

## 3. Flujo General de Procesamiento

1. El usuario ubica los archivos fuente en `input/`.
2. Al ejecutar el script principal (`main.py`), se activa el pipeline:
   - Procesa primero los archivos de flujos y estimaciones, generando un nuevo archivo de flujos actualizado.
   - Posteriormente, se actualiza el archivo de informe (R5) usando la versión procesada del flujo.
   - Todo el proceso se registra en el log para trazabilidad y depuración.
3. Los resultados finales se guardan en `output/`.

---

## 4. Descripción de los Módulos

### 4.1 main.py

- **Rol:** Punto de entrada del proceso automático. Orquesta las llamadas a los módulos principales.
- **Lógica:**
  - Inicializa logging y directorios.
  - Llama a la función para procesar los flujos de swaps (`procesar_swaps.py`).
  - Llama a la función para actualizar el informe R5 (`actualizar_informe.py`) usando el flujo ya procesado.
  - Controla el flujo de errores, registro de eventos y reporta el final de la ejecución.
- **Fragmento clave:**
  ```python
  from pkg.procesar_swaps import procesar_archivos_swaps
  from pkg.actualizar_informe import actualizar_informe

  # Procesar los archivos de swaps
  procesar_archivos_swaps(input_dir, output_dir)

  # Actualizar el informe R5 con el archivo de flujos ya procesado
  actualizar_informe(output_dir, input_dir)
  ```

### 4.2 pkg/procesar\_swaps.py

- **Rol:** Núcleo de la lógica de procesamiento de los archivos de flujos y estimaciones.
- **Lógica:**
  - Lee el archivo de flujos de swaps y el archivo de estimaciones (ambos separados por punto y coma).
  - Aplica reglas de transformación y actualización de campos según las necesidades del negocio.
  - Escribe el archivo de flujos ya procesado en la carpeta `output/`.
  - Usa funciones de utilidad (`utils.py`) para tareas repetitivas como validaciones, conversión de datos y limpieza de caracteres especiales.
- **Funciones destacadas:**
  - `procesar_archivos_swaps(input_dir, output_dir)`: Orquesta todo el procesamiento, llama a funciones de lectura, transformación y guardado.
  - Validación de caracteres, normalización de datos y registro de cambios.

### 4.3 pkg/utils.py

- **Rol:** Conjunto de utilidades auxiliares, facilita operaciones comunes.
- **Funciones típicas:**
  - Limpieza de caracteres no deseados (por ejemplo, cambio de ñ por n, eliminación de tildes).
  - Conversión de formatos de fecha y valores numéricos.
  - Validaciones de campos y consistencia de datos.
  - Otras funciones auxiliares reutilizadas por los módulos principales.

### 4.4 pkg/actualizar\_informe.py

- **Rol:** Encargado de actualizar el archivo de informe R5 (Reporte final) usando los datos transformados del archivo de flujos ya procesado.
- **Lógica:**
  - Lee el archivo de informe original y el archivo de flujos procesado.
  - Cruza la información usando campos clave.
  - Actualiza campos específicos (por ejemplo, cupones, fechas, tasas) según reglas de negocio.
  - Guarda el informe actualizado en `output/`.
  - Registra advertencias y errores (por ejemplo, cambios de tipo de dato no compatibles).

---

## 5. Ejecución y Uso

1. Instala las dependencias necesarias:
   ```bash
   pip install pandas
   ```
2. Coloca los archivos fuente (.csv, .dat) en la carpeta `input/`.
3. Ejecuta el proceso desde la terminal:
   ```bash
   cd code
   python main.py
   ```
4. Los archivos generados se encontrarán en `output/`, y el log del proceso en `logs/swaps.log`.

---

## 6. Buenas Prácticas y Observaciones

- El código sigue principios de modularidad: cada responsabilidad está separada por archivo y función.
- Usa logging profesional para registrar el proceso y facilitar la trazabilidad y depuración.
- Usa funciones de utilidad para evitar repetición de código.
- La estructura es escalable: puedes agregar nuevas reglas o archivos sin modificar mucho el código base.
- Incluye `.gitignore` y `.env` para gestión de entorno y seguridad.

---

## 7. Mejoras Potenciales y Recomendaciones

- **Validaciones adicionales:** Incluir pruebas automáticas de validación de datos y formatos antes de procesar los archivos.
- **Automatización:** Integrar con herramientas de orquestación (Airflow, cron) si se requiere ejecución periódica.
- **Parámetros por CLI:** Permitir pasar rutas o fechas por argumentos para mayor flexibilidad.
- **Control de versiones de archivos:** Versionar archivos de entrada y salida para trazabilidad histórica.
- **Documentación extendida:** Ampliar el README con ejemplos detallados de entrada/salida.
- **Soporte para otros formatos:** Permitir procesamiento de archivos con otros delimitadores o extensiones.
- **Test unitarios:** Agregar pruebas unitarias para funciones críticas.

---

**Fin del manual.**

