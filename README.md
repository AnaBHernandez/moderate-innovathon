# MODERATE - Predicción semanal de consumo de biomasa

## Cómo ejecutar

### 1) Inspección de datos (opcional)
```bash
python3 /workspace/scripts/inspect_data.py
```

### 2) Predicción semanal por CLI
```bash
python3 -m src.predict_weekly --inst all --lat 40.9701039 --lon -5.6635397 \
  --out /workspace/Entregables/prediccion_semanal.json
```

### 3) Dashboard (Streamlit)
```bash
python3 -m streamlit run /workspace/app/dashboard.py --server.headless true \
  --server.port 8501 --server.address 0.0.0.0
```

## Estructura
- `src/data_ingest.py`: carga HDD, energía y descargas de biomasa (openpyxl), genera series diarias/semanales.
- `src/modeling.py`: modelos lineales (numpy.polyfit) por instalación y factor biomasa (t/MWh).
- `src/aemet.py`: HDD próximos 7 días (Open-Meteo; AEMET opcional con API key).
- `src/predict_weekly.py`: CLI de predicción y JSON de salida.
- `app/dashboard.py`: dashboard Streamlit.
- `scripts/inspect_data.py`: vista previa de estructura de Excel.
