# Diccionario de variables

| Variable | Definición | Unidad de medida | Frecuencia | Fuente | URL o endpoint de origen |
|----------|------------|------------------|------------|--------|--------------------------|
| `fecha` | Fecha de la observación | Fecha | Diaria | — | — |
| `retorno_emb` | Cambio porcentual diario del precio de cierre del ETF EMB | % | Diaria | Yahoo Finance (calculado) | https://finance.yahoo.com/quote/EMB |
| `precio_emb` | Precio de cierre del ETF EMB | USD | Diaria | Yahoo Finance | https://finance.yahoo.com/quote/EMB |
| `volumen` | Volumen de negociación del ETF EMB | Acciones | Diaria | Yahoo Finance | https://finance.yahoo.com/quote/EMB |
| `tasa_10a` | Tasa del Tesoro de EE. UU. a 10 años (DGS10) | % | Diaria | FRED | https://fred.stlouisfed.org/series/DGS10 |
| `vix` | Índice de volatilidad VIX (VIXCLS) | Puntos | Diaria | FRED | https://fred.stlouisfed.org/series/VIXCLS |
| `embig_peru` | Spread del EMBIG Perú (PD04709XD) | Puntos básicos | Diaria | BCRP | https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04709XD/json |

---

## Notas

- **Período de análisis:** 2014-01-01 a 2025-12-31.
- **Número de observaciones:** 3 016.
- **Frecuencia:** Diaria.
- **Llave común para unir las fuentes:** `fecha`.
- **Tratamiento de valores faltantes:** Interpolación lineal para DGS10, VIX y EMBIG Perú.
- **Cálculo del retorno:** `retorno_emb = (precio_emb_t - precio_emb_{t-1}) / precio_emb_{t-1} * 100`.