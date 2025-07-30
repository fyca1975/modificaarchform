import os
import pandas as pd
import logging

def extraer_fecha(nombre):
    """Extrae la fecha del nombre de archivo y la retorna en (aaaa, mm, dd)"""
    # flujos_swap_gbo_aaaammdd.csv
    base = os.path.basename(nombre)
    if "flujos_swap_gbo" in base:
        fecha = base.split("_")[-1].split(".")[0]
        return fecha[:4], fecha[4:6], fecha[6:8]
    # COL_ESTIM_FLOWS_ddmmaaaa.dat
    if "COL_ESTIM_FLOWS" in base:
        fecha = base.split("_")[-1].split(".")[0]
        return fecha[4:8], fecha[2:4], fecha[0:2]
    return None, None, None

def procesar_swaps(input_dir, output_dir):
    try:
        # Buscar archivos de entrada
        archivos = os.listdir(input_dir)
        flujo_csv = [f for f in archivos if f.startswith("flujos_swap_gbo") and f.endswith(".csv")]
        dat = [f for f in archivos if f.startswith("COL_ESTIM_FLOWS") and f.endswith(".dat")]

        if not flujo_csv or not dat:
            logging.error("No se encontraron archivos de flujos o estimaciones en input/")
            return None, None

        flujo_csv = flujo_csv[0]
        dat = dat[0]

        # Validar fechas
        a1, m1, d1 = extraer_fecha(flujo_csv)
        a2, m2, d2 = extraer_fecha(dat)
        if not (a1 == a2 and m1 == m2 and d1 == d2):
            logging.error(f"Fechas no coinciden entre archivos: {flujo_csv} y {dat}")
            return None, None

        fecha_str = f"{a1}{m1}{d1}"

        # Leer archivos
        df_flujo = pd.read_csv(os.path.join(input_dir, flujo_csv), sep=';', encoding='latin1')
        df_dat = pd.read_csv(os.path.join(input_dir, dat), sep=';', encoding='latin1')

        # Validaciones
        if df_flujo.empty or df_dat.empty:
            logging.error("Algún archivo está vacío.")
            return None, None

        # Procesar y actualizar
        for i, row in df_dat.iterrows():
            matches = (df_flujo['cod_emp'] == str(row['M_CONTRACT_'])) &                       (df_flujo['fecha_cobro'] == str(row['M_DATE']))
            idxs = df_flujo.index[matches]
            for idx in idxs:
                # Reglas de negocio
                if row['M_DISCFLOWC'] > 0:
                    df_flujo.at[idx, 'der_vp'] = float(row['M_DISCFLOWC'])
                elif row['M_DISCFLOWC'] < 0:
                    df_flujo.at[idx, 'obl_vp'] = abs(float(row['M_FLOW_COL']))
                if row['M_FLOW_COL'] > 0:
                    df_flujo.at[idx, 'der_intereses'] = float(row['M_FLOW_COL'])
                elif row['M_FLOW_COL'] < 0:
                    df_flujo.at[idx, 'obl_intereses'] = abs(float(row['M_DISCFLOWC']))

        # Guardar modificado
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, flujo_csv)
        df_flujo.to_csv(output_path, sep=';', index=False, encoding='latin1')
        logging.info(f"Archivo de flujos modificado guardado en {output_path}")
        return flujo_csv, fecha_str

    except Exception as e:
        logging.exception(f"Error procesando flujos: {e}")
        return None, None
