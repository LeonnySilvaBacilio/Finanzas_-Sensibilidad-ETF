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
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan
import matplotlib.pyplot as plt
import seaborn as sns

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
log.write(f"[{datetime.now()}] INICIO DE ANÁLISIS\n")
log.write(f"{'='*60}\n")

# ============================================================
# 1. CARGAR DATOS PROCESADOS
# ============================================================
print("📂 Cargando datos procesados...")

df = pd.read_csv(f"{RUTA}/datos_procesados/datos_procesados_{CODIGO_MATRICULA}.csv")
df['fecha'] = pd.to_datetime(df['fecha'])

print(f"   Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

# ============================================================
# 2. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================
print("\n📊 Estadísticas descriptivas...")

desc = df[['retorno_emb', 'tasa_10a', 'vix', 'embig_peru', 'volumen']].describe()
desc.to_csv(f"{RUTA}/salidas/tabla_descriptivas.csv")

# ============================================================
# 3. MATRIZ DE CORRELACIÓN
# ============================================================
print("\n🔗 Calculando matriz de correlación...")

corr = df[['retorno_emb', 'tasa_10a', 'vix', 'embig_peru', 'volumen']].corr()
corr.to_csv(f"{RUTA}/salidas/tabla_correlacion.csv")

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.3f')
plt.title('Matriz de Correlación')
plt.tight_layout()
plt.savefig(f"{RUTA}/salidas/figura_correlacion.png", dpi=300)
plt.close()
print("   ✅ Figura de correlación guardada")

# ============================================================
# 4. MODELO DE REGRESIÓN (ORIGINAL Y ROBUSTO)
# ============================================================
print("\n📈 Estimando modelo de regresión...")

X = df[['tasa_10a', 'vix', 'embig_peru', 'volumen']]
y = df['retorno_emb']
X = sm.add_constant(X)

modelo_original = sm.OLS(y, X).fit()
modelo_robusto = sm.OLS(y, X).fit(cov_type='HC3')

with open(f"{RUTA}/salidas/tabla_regresion_original.txt", "w") as f:
    f.write(modelo_original.summary().as_text())

with open(f"{RUTA}/salidas/tabla_regresion_robusta.txt", "w") as f:
    f.write(modelo_robusto.summary().as_text())

print("   ✅ Modelos guardados")

# ============================================================
# 5. PRUEBAS DE SUPUESTOS
# ============================================================
print("\n🔬 Pruebas de supuestos...")

residuos = modelo_original.resid

dw = durbin_watson(residuos)
bp_test = het_breuschpagan(residuos, modelo_original.model.exog)
jb_test = jarque_bera(residuos)

with open(f"{RUTA}/salidas/tabla_pruebas.txt", "w") as f:
    f.write(f"Durbin-Watson: {dw:.4f}\n")
    f.write(f"Breusch-Pagan p-valor: {bp_test[1]:.4f}\n")
    f.write(f"Jarque-Bera p-valor: {jb_test[1]:.4f}\n")

print(f"   Durbin-Watson: {dw:.4f}")
print(f"   Breusch-Pagan p-valor: {bp_test[1]:.4f}")
print(f"   Jarque-Bera p-valor: {jb_test[1]:.4f}")

# ============================================================
# 6. FIGURA: SERIES DE TIEMPO
# ============================================================
print("\n🎨 Generando figura de series de tiempo...")

df_norm = df.copy()
for var in ['retorno_emb', 'tasa_10a', 'vix', 'embig_peru', 'volumen']:
    df_norm[f'{var}_norm'] = (df[var] - df[var].mean()) / df[var].std()

plt.figure(figsize=(14, 7))
plt.plot(df_norm['fecha'], df_norm['retorno_emb_norm'], label='Retorno EMB', color='blue', linewidth=1)
plt.plot(df_norm['fecha'], df_norm['tasa_10a_norm'], label='Tasa 10A', color='red', linewidth=1)
plt.plot(df_norm['fecha'], df_norm['vix_norm'], label='VIX', color='orange', linewidth=1)
plt.plot(df_norm['fecha'], df_norm['embig_peru_norm'], label='EMBIG Perú', color='green', linewidth=1)
plt.plot(df_norm['fecha'], df_norm['volumen_norm'], label='Volumen', color='purple', linewidth=1)
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
plt.title('Evolución de las 5 variables (normalizadas)')
plt.xlabel('Fecha')
plt.ylabel('Desviaciones estándar')
plt.legend()
plt.tight_layout()
plt.savefig(f"{RUTA}/salidas/figura_series_tiempo.png", dpi=300)
plt.close()
print("   ✅ Figura de series de tiempo guardada")

# ============================================================
# 7. FIGURAS: DISPERSIÓN INDIVIDUAL
# ============================================================
print("\n🎨 Generando gráficos de dispersión...")

variables = ['tasa_10a', 'vix', 'embig_peru', 'volumen']
titulos = ['Tasa del Tesoro 10A', 'VIX', 'EMBIG Perú', 'Volumen']
colores = ['red', 'orange', 'green', 'purple']

for var, titulo, color in zip(variables, titulos, colores):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[var], df['retorno_emb'], alpha=0.3, color=color)
    plt.xlabel(titulo)
    plt.ylabel('Retorno del EMB')
    plt.title(f'Retorno del EMB vs. {titulo}')
    plt.tight_layout()
    plt.savefig(f"{RUTA}/salidas/figura_dispersion_{var}.png", dpi=300)
    plt.close()
    print(f"   ✅ Figura de dispersión vs. {titulo} guardada")

# ============================================================
# 8. CIERRE
# ============================================================
log.write(f"[{datetime.now()}] Análisis completado\n")
log.write(f"[{datetime.now()}] FIN DE ANÁLISIS\n")
log.write(f"{'='*60}\n")
log.close()

print("\n" + "="*60)
print("ANÁLISIS COMPLETADO")
print("="*60)
print(f"Resultados guardados en: {RUTA}/salidas/")
