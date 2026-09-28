# SILVA BACILIO LEONNY YUVELI
# 2024200528H
# Tema 55: Sensibilidad de un ETF de deuda emergente a la tasa libre de riesgo y al riesgo país
# Fecha de extracción: 2026-09-28

# ============================================================
# IMPORTAR LIBRERÍAS
# ============================================================
import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from fredapi import Fred
import time

# ============================================================
# PARÁMETROS CONGELADOS
# ============================================================
FECHA_INICIO = "2014-01-01"
FECHA_CORTE = "2025-12-31"
TICKER_ETF = "EMB"
SERIE_TASA = "DGS10"
SERIE_VIX = "VIXCLS"
CODIGO_MATRICULA = "2024200528H"

# Ruta del proyecto en Drive
RUTA = "/content/drive/MyDrive/SILVA BACILIO LEONNY YUVELI/N°3 BASE DE DATOS Y CÓDIGOS SILVA BACILIO LEONNY"

# ============================================================
# PREPARAR LOG
# ============================================================
log = open(f"{RUTA}/log_ejecucion.txt", "a", encoding="utf-8")
log.write(f"\n{'='*60}\n")
log.write(f"[{datetime.now()}] INICIO DE EXTRACCIÓN POR API\n")
log.write(f"{'='*60}\n")

# ============================================================
# EXTRACCIÓN 1: Yahoo Finance - ETF EMB
# ============================================================
log.write(f"\n[{datetime.now()}] Extrayendo {TICKER_ETF} desde Yahoo Finance...\n")

try:
    time.sleep(1)
    emb = yf.download(TICKER_ETF, start=FECHA_INICIO, end=FECHA_CORTE, progress=False, auto_adjust=False)
    
    if emb.empty:
        raise ValueError("No se descargaron datos del ETF")
    
    archivo_emb = f"{RUTA}/datos_crudos/datos_crudos_{TICKER_ETF}_{CODIGO_MATRICULA}.csv"
    emb.to_csv(archivo_emb)
    
    log.write(f"[{datetime.now()}] {TICKER_ETF} extraído: {len(emb)} filas, HTTP 200\n")
    print(f"✅ {TICKER_ETF} extraído: {len(emb)} filas")

except Exception as e:
    log.write(f"[{datetime.now()}] ❌ ERROR al extraer {TICKER_ETF}: {e}\n")
    print(f"❌ Error al extraer {TICKER_ETF}: {e}")

# ============================================================
# EXTRACCIÓN 2: FRED - DGS10 y VIXCLS
# ============================================================
log.write(f"\n[{datetime.now()}] Conectando a FRED...\n")

try:
    api_key = os.environ.get("FRED_API_KEY")
    
    if not api_key:
        raise ValueError("No se encontró FRED_API_KEY")
    
    fred = Fred(api_key=api_key)
    
    # --- DGS10 ---
    time.sleep(1)
    dgs10 = fred.get_series(SERIE_TASA, observation_start=FECHA_INICIO, observation_end=FECHA_CORTE)
    archivo_dgs10 = f"{RUTA}/datos_crudos/datos_crudos_{SERIE_TASA}_{CODIGO_MATRICULA}.csv"
    dgs10.to_csv(archivo_dgs10, header=["valor"])
    print(f"✅ {SERIE_TASA} extraído: {len(dgs10)} filas")
    
    # --- VIXCLS ---
    time.sleep(1)
    vix = fred.get_series(SERIE_VIX, observation_start=FECHA_INICIO, observation_end=FECHA_CORTE)
    archivo_vix = f"{RUTA}/datos_crudos/datos_crudos_{SERIE_VIX}_{CODIGO_MATRICULA}.csv"
    vix.to_csv(archivo_vix, header=["valor"])
    print(f"✅ {SERIE_VIX} extraído: {len(vix)} filas")

except Exception as e:
    log.write(f"[{datetime.now()}] ❌ ERROR en FRED: {e}\n")
    print(f"❌ Error en FRED: {e}")

# ============================================================
# CIERRE
# ============================================================
log.close()
print("\n" + "="*60)
print("EXTRACCIÓN POR API COMPLETADA")
print("="*60)
