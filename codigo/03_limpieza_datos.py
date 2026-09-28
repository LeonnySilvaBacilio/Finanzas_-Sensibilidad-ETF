# SILVA BACILIO LEONNY YUVELI
# 2024200528H
# Tema 55: Sensibilidad de un ETF de deuda emergente a la tasa libre de riesgo y al riesgo país
# Fecha de extracción: 2026-09-28

# ============================================================
# IMPORTAR LIBRERÍAS
# ============================================================
import pandas as pd
import numpy as np
import os
from datetime import datetime

# ============================================================
# PARÁMETROS
# ============================================================
CODIGO_MATRICULA = "2024200528H"
RUTA = "/content/drive/MyDrive/SILVA BACILIO LEONNY YUVELI/N°3 BASE DE DATOS Y CÓDIGOS SILVA BACILIO LEONNY"

# ============================================================
# ABRIR LOG
# ============================================================
log = open(f"{RUTA}/log_ejecucion.txt", "a", encoding="utf-8")
log.write(f"\n{'='*60}\n")
log.write(f"[{datetime.now()}] INICIO DE LIMPIEZA DE DATOS\n")
log.write(f"{'='*60}\n")

# ============================================================
# 1. CARGAR EMB
# ============================================================
print("📂 Cargando EMB...")

emb = pd.read_csv(
    f"{RUTA}/datos_crudos/datos_crudos_EMB_{CODIGO_MATRICULA}.csv",
    skiprows=2
)

emb.columns = ['fecha', 'adj_close', 'precio_emb', 'high', 'low', 'open', 'volumen']
emb['fecha'] = pd.to_datetime(emb['fecha'], errors='coerce')
emb['precio_emb'] = pd.to_numeric(emb['precio_emb'], errors='coerce')
emb['volumen'] = pd.to_numeric(emb['volumen'], errors='coerce')
emb = emb[['fecha', 'precio_emb', 'volumen']]
emb = emb.dropna(subset=['fecha'])

print(f"   EMB limpio: {emb.shape[0]} filas, {emb.shape[1]} columnas")

# ============================================================
# 2. CARGAR DGS10
# ============================================================
print("\n📂 Cargando DGS10...")

dgs10 = pd.read_csv(f"{RUTA}/datos_crudos/datos_crudos_DGS10_{CODIGO_MATRICULA}.csv")
dgs10.columns = ['fecha', 'tasa_10a']
dgs10['fecha'] = pd.to_datetime(dgs10['fecha'], errors='coerce')
dgs10['tasa_10a'] = pd.to_numeric(dgs10['tasa_10a'], errors='coerce')
dgs10 = dgs10.dropna(subset=['fecha'])

print(f"   DGS10 limpio: {dgs10.shape[0]} filas, {dgs10.shape[1]} columnas")

# ============================================================
# 3. CARGAR VIXCLS
# ============================================================
print("\n📂 Cargando VIXCLS...")

vix = pd.read_csv(f"{RUTA}/datos_crudos/datos_crudos_VIXCLS_{CODIGO_MATRICULA}.csv")
vix.columns = ['fecha', 'vix']
vix['fecha'] = pd.to_datetime(vix['fecha'], errors='coerce')
vix['vix'] = pd.to_numeric(vix['vix'], errors='coerce')
vix = vix.dropna(subset=['fecha'])

print(f"   VIXCLS limpio: {vix.shape[0]} filas, {vix.shape[1]} columnas")

# ============================================================
# 4. CARGAR EMBIG PERÚ
# ============================================================
print("\n📂 Cargando EMBIG Perú...")

embig = pd.read_csv(f"{RUTA}/datos_crudos/datos_crudos_PD04709XD_{CODIGO_MATRICULA}.csv")
embig['fecha'] = pd.to_datetime(embig['fecha'], errors='coerce')
embig['embig_peru'] = pd.to_numeric(embig['embig_peru'], errors='coerce')
embig = embig.dropna(subset=['fecha'])

print(f"   EMBIG limpio: {embig.shape[0]} filas, {embig.shape[1]} columnas")

# ============================================================
# 5. UNIR TODAS LAS FUENTES
# ============================================================
print("\n🔗 Uniendo fuentes...")

df = pd.merge(emb, dgs10, on='fecha', how='left')
df = pd.merge(df, vix, on='fecha', how='left')
df = pd.merge(df, embig, on='fecha', how='left')

print(f"   Después de unir todas las fuentes: {df.shape[0]} filas")

# ============================================================
# 6. CALCULAR RETORNO
# ============================================================
print("\n📈 Calculando retorno...")

df['retorno_emb'] = df['precio_emb'].pct_change() * 100

# ============================================================
# 7. TRATAR VALORES FALTANTES
# ============================================================
print("\n🔧 Tratando valores faltantes...")

print("   Valores nulos antes de imputación:")
print(df.isnull().sum())

df['tasa_10a'] = df['tasa_10a'].interpolate(method='linear')
df['vix'] = df['vix'].interpolate(method='linear')
df['embig_peru'] = df['embig_peru'].interpolate(method='linear')

df = df.dropna(subset=['retorno_emb'])

print("\n   Valores nulos después de imputación:")
print(df.isnull().sum())

# ============================================================
# 8. ORDENAR Y GUARDAR
# ============================================================
print("\n💾 Guardando datos procesados...")

df = df[['fecha', 'retorno_emb', 'precio_emb', 'volumen', 'tasa_10a', 'vix', 'embig_peru']]
df = df.sort_values('fecha').reset_index(drop=True)

archivo_procesado = f"{RUTA}/datos_procesados/datos_procesados_{CODIGO_MATRICULA}.csv"
df.to_csv(archivo_procesado, index=False)

print(f"   ✅ Archivo guardado: {archivo_procesado}")
print(f"   Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

# ============================================================
# 9. VERIFICAR REQUISITOS
# ============================================================
print("\n📋 Verificando requisitos de la rúbrica:")
print(f"   ✅ Mínimo 6 columnas: {df.shape[1]} columnas")
print(f"   ✅ Mínimo 1000 observaciones: {df.shape[0]} filas")
print(f"   ✅ Variables sustantivas: {df.shape[1] - 1}")
print(f"   ✅ Fuentes: Yahoo Finance, FRED, BCRP")

log.write(f"[{datetime.now()}] Limpieza completada: {df.shape[0]} filas, {df.shape[1]} columnas\n")
log.write(f"[{datetime.now()}] FIN DE LIMPIEZA DE DATOS\n")
log.write(f"{'='*60}\n")
log.close()

print("\n" + "="*60)
print("LIMPIEZA DE DATOS COMPLETADA")
print("="*60)
