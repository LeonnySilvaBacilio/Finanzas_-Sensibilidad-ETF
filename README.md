# Proyecto: Sensibilidad de un ETF de deuda emergente a la tasa libre de riesgo y al riesgo país
**Autor:** SILVA BACILIO LEONNY YUVELI
**Código de matrícula:** 2024200528H
**Tema:** Tema 55 — Sensibilidad de un ETF de deuda emergente a la tasa libre de riesgo y al riesgo país
**Curso:** Finanzas I — Código 055D — Ciclo V
**Docente:** Dr. Ciro Iván Machacuay Meza
**Institución:** Universidad Nacional del Centro del Perú — Facultad de Economía
**Período lectivo:** 2026-II

---

## Descripción del proyecto

Este proyecto estima la sensibilidad del retorno del ETF EMB (iShares J.P. Morgan USD Emerging Markets Bond ETF) a shocks en la tasa libre de riesgo (DGS10), el VIX, el riesgo país de Perú (EMBIG) y el volumen de negociación, durante el período 2014-2025.
La base de datos fue construida mediante extracción automatizada de Yahoo Finance (API), FRED (API) y el BCRP (API). Se estimó un modelo de regresión lineal múltiple con errores estándar robustos HC3.

---

## Estructura del proyecto
N.º 3 - Base de datos y codigo - SILVA BACILIO LEONNY YUVELI/
│
├── codigo/
│ ├── 01_extraccion_api.py
│ ├── 02_scraping_web.py
│ ├── 03_limpieza_datos.py
│ └── 04_analisis.py
│
├── datos_crudos/
│ ├── datos_crudos_EMB_2024200528H.csv
│ ├── datos_crudos_DGS10_2024200528H.csv
│ ├── datos_crudos_VIXCLS_2024200528H.csv
│ └── datos_crudos_PD04709XD_2024200528H.csv
│
├── datos_procesados/
│ └── datos_procesados_2024200528H.csv
│
├── salidas/
│ ├── tabla_descriptivas.csv
│ ├── tabla_correlacion.csv
│ ├── tabla_regresion_original.txt
│ ├── tabla_regresion_robusta.txt
│ ├── tabla_pruebas.txt
│ ├── figura_correlacion.png
│ ├── figura_series_tiempo.png
│ ├── figura_dispersion_tasa_10a.png
│ ├── figura_dispersion_vix.png
│ ├── figura_dispersion_embig_peru.png
│ └── figura_dispersion_volumen.png
│
├── .env.example
├── README.md
├── requirements.txt
├── log_ejecucion.txt
└── diccionario_variables.xlsx


---

## Fuentes de datos y endpoints

| Variable | Fuente | Endpoint / Ticker | Fecha de corte |
|----------|--------|-------------------|----------------|
| Precio y volumen del EMB | Yahoo Finance (yfinance) | `EMB` | 2025-12-31 |
| Tasa del Tesoro 10A (DGS10) | FRED API | `DGS10` | 2025-12-31 |
| VIX (VIXCLS) | FRED API | `VIXCLS` | 2025-12-31 |
| EMBIG Perú (PD04709XD) | BCRP API | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04709XD/json` | 2025-12-31 |

---

## Orden de ejecución

Los scripts deben ejecutarse en el siguiente orden:

1. `01_extraccion_api.py` — Extrae EMB, DGS10 y VIXCLS.
2. `02_scraping_web.py` — Extrae el EMBIG Perú desde el BCRP.
3. `03_limpieza_datos.py` — Limpia, une las fuentes y genera el archivo procesado.
4. `04_analisis.py` — Estima la regresión, genera tablas y figuras.

---

## Instalación y requisitos

### Python

Se utilizó **Python 3.11**. Las librerías y versiones exactas se encuentran en `requirements.txt`.

Para instalar las dependencias:

```bash
pip install -r requirements.txt


##Hash SHA-256 del archivo
0d9b1b6c8c04f7a1ac65eef89667d60d2ac0cb0560bff728652b3e004b42150a

#Incidencias
Primer Incidencia: Durante la extracción de la serie del EMBIG Perú (código PD04709XD) mediante la API del BCRP, se obtuvo inicialmente solo 90 observaciones, correspondientes a un rango de fechas de aproximadamente tres meses (desde enero de 2026 hasta marzo de 2026). Esto ocurrió porque el endpoint utilizado por defecto devolvía únicamente los últimos 90 días de la serie, sin permitir especificar un rango histórico completo. Como consecuencia, al unir esta serie con las demás fuentes (EMB, DGS10 y VIXCLS), el 99.9\% de las filas del archivo procesado quedaban con valores nulos en la columna `embig_peru`, lo que impedía el análisis de sensibilidad. Para solucionar este problema, se investigó la estructura de la API del BCRP y se identificó que el formato correcto de la URL debía incluir el rango de fechas en la ruta, no como parámetro de consulta. El endpoint correcto resultó ser:
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04709XD/json/2014-01-01/2025-12-31
Con este formato, se obtuvo la serie completa del EMBIG Perú con 3 131 observaciones, cubriendo el período 2014-2025. Posteriormente, se aplicó un proceso de parseo de fechas (del formato `01.Ene.14` a `2014-01-01`) y limpieza de valores (eliminación de corchetes) en el script `03_limpieza_datos.py`. Finalmente, se aplicó una interpolación lineal para rellenar los 22 valores faltantes correspondientes a días festivos en los que el BCRP no publicó datos, pero la bolsa de valores sí operó.


Segunda Incidencia: Durante la ejecución del proyecto, se presentaron diversas incidencias tanto en el manejo y extracción de datos así como problemas externos. El desarrollo de códigos para la extracción de datos fue manejado a un inicio en la IA Claude (versión pro) hasta el día 25/09/2026; debido a que la cuenta era compartida, la seguridad de los datos era leve; en la fecha mencionada, se observó que la carpeta de trabajo había sido eliminada, y como no se contaba con el total de la cuenta, no se pudo recuperar el avance alcanzado. Por tal motivo, la IA predeterminada para la extracción y análisis de datos fue DeepSeek (Que había sido utilizada únicamente como una guía de apoyo para prueba de los códigos, fue derivada como principal apoyo en codificación). 

Tercer Incidencia: De manera similar, los 2 primeros commits fueron trabados en fechas 23/09/2026 y 24/09/2026 en una cuenta diferente a la usada en el actual trabajo; se tenía planificado usar aquella cuenta como predeterminada para el manejo de commits, sin embargo, el almacenamiento lleno imposibilitó el acceso a las contraseñas en GitHub por lo que tuvo que recurrir a hacer uso de una cuenta secundaria. Ante ello, se planificó volver a subir los commits en las fechas 28/09/2026, 29/09/2026 y 28/09/2026; sin embargo, el cronograma de entregas fue modificado, de tal manera que la fecha límite cambió  a 28/09/2026.

##Variables de entorno
El proyecto requiere una API Key de FRED. Se debe crear un archivo .env en la raíz del proyecto con el siguiente contenido:

text
FRED_API_KEY=tu_clave_aqui
Se incluye un archivo .env.example como plantilla. No se debe subir el archivo .env al repositorio (está en .gitignore).

Para obtener una API Key de FRED: https://fred.stlouisfed.org/docs/api/api_key.html

##Repositorio GitHub
https://github.com/LeonnySilvaBacilio/Finanzas_-Sensibilidad-ETF

El repositorio contiene:

Los 4 scripts de Python.

Los archivos de datos crudos y procesados.

Las tablas y figuras generadas.

El diccionario de variables.

El presente README.

##Nota sobre el cronograma
El cronograma original del curso se adelantó por disposición del docente. Debido a ello, la extracción de datos se ejecutó el 28 de septiembre de 2026, y los commits se realizaron en la misma fecha. El log de ejecución (log_ejecucion.txt) acredita la fecha y hora exactas de cada extracción.


##Licencia
Este proyecto es de uso académico exclusivamente. Todos los datos empleados son públicos y verificables en las fuentes oficiales declaradas.

##Contacto
Autor: SILVA BACILIO LEONNY YUVELI
Correo: e_2024200528@uncp.edu.pe
Institución: Universidad Nacional del Centro del Perú