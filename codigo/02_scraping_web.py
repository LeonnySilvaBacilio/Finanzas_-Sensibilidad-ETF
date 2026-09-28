# SILVA BACILIO LEONNY YUVELI
# 2024200528H
# Tema 55: Sensibilidad de un ETF de deuda emergente a la tasa libre de riesgo y al riesgo país
# Fecha de extracción: 2026-09-28

# ============================================================
# IMPORTAR LIBRERÍAS
# ============================================================
import requests
import pandas as pd
import os
from datetime import datetime
import time
import json

# ============================================================
# PARÁMETROS CONGELADOS
# ============================================================
FECHA_INICIO = "2014-01-01"
FECHA_CORTE = "2025-12-31"
SERIE_EMBIG = "PD04709XD"
CODIGO_MATRICULA = "2024200528H"

# Ruta del proyecto en Drive
RUTA = "/content/drive/MyDrive/SILVA BACILIO LEONNY YUVELI/N°3 BASE DE DATOS Y CÓDIGOS SILVA BACILIO LEONNY"

# ============================================================
# ABRIR EL LOG
# ============================================================
log = open(f"{RUTA}/log_ejecucion.txt", "a", encoding="utf-8")
log.write(f"\n{'='*60}\n")
log.write(f"[{datetime.now()}] INICIO DE EXTRACCIÓN EMBIG PERÚ (BCRP)\n")
log.write(f"{'='*60}\n")

# ============================================================
# EXTRACCIÓN: EMBIG Perú desde BCRP
# ============================================================
log.write(f"\n[{datetime.now()}] Extrayendo {SERIE_EMBIG} desde BCRP...\n")

try:
    time.sleep(1)
    
    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{SERIE_EMBIG}/json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Academico UNCP; contacto@uncp.edu.pe)"
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    
    log.write(f"[{datetime.now()}] Respuesta HTTP: {response.status_code}\n")
    
    if response.status_code != 200:
        raise ValueError(f"Error HTTP: {response.status_code}")
    
    data = response.json()
    
    # Extraer la lista de períodos
    lista_datos = data['periods']
    
    # Convertir a DataFrame
    df = pd.DataFrame(lista_datos)
    
    # Guardar el archivo crudo
    archivo_embig = f"{RUTA}/datos_crudos/datos_crudos_{SERIE_EMBIG}_{CODIGO_MATRICULA}.csv"
    df.to_csv(archivo_embig, index=False)
    
    log.write(f"[{datetime.now()}] {SERIE_EMBIG} extraído: {len(df)} filas\n")
    log.write(f"[{datetime.now()}] Archivo guardado: {archivo_embig}\n")
    print(f"✅ {SERIE_EMBIG} extraído: {len(df)} filas")

except Exception as e:
    log.write(f"[{datetime.now()}] ❌ ERROR al extraer {SERIE_EMBIG}: {e}\n")
    print(f"❌ Error al extraer {SERIE_EMBIG}: {e}")

# ============================================================
# CIERRE
# ============================================================
log.write(f"\n[{datetime.now()}] FIN DE EXTRACCIÓN EMBIG PERÚ\n")
log.write(f"{'='*60}\n")
log.close()

print("\n" + "="*60)
print("EXTRACCIÓN EMBIG PERÚ COMPLETADA")
print("="*60)
