from __future__ import annotations
import json
from pathlib import Path
from typing import Dict

import os
os.environ['PYTHONWARNINGS'] = 'ignore'

import streamlit as st

from src.modeling import build_models
from src.aemet import compute_hdd_next7

DEFAULT_BASE = Path('/workspace/datos_originales')
DEFAULT_LAT = 40.9701039
DEFAULT_LON = -5.6635397

st.set_page_config(page_title='MODERATE - Biomasa', layout='wide')
st.title('Predicción semanal de biomasa por instalación')

colA, colB = st.columns([2,1])
with colA:
    base_dir_text = st.text_input('Carpeta de datos', str(DEFAULT_BASE))
base_dir = Path(base_dir_text)

# Cargar modelos
with st.spinner('Entrenando modelos...'):
    energy_models, biomass_model, baseline_energy = build_models(base_dir)

inst_list = sorted(energy_models.keys())
col1, col2, col3 = st.columns([2,1,1])
with col1:
    inst = st.selectbox('Instalación', options=['Todas'] + inst_list)
with col2:
    lat = st.number_input('Latitud', value=DEFAULT_LAT, format='%.6f')
with col3:
    lon = st.number_input('Longitud', value=DEFAULT_LON, format='%.6f')

hdd7 = compute_hdd_next7(lat, lon)
st.subheader('HDD próximos 7 días')
st.bar_chart(hdd7)

from src.modeling import predict_week_energy

results = []
if inst == 'Todas':
    targets = inst_list
else:
    targets = [inst]

for i in targets:
    em = energy_models[i]
    energy = predict_week_energy(hdd7, em, baseline_energy.get(i, 0.0))
    biom = energy * biomass_model.factor_ton_per_mwh
    results.append({'instalacion': i, 'energia_MWh': round(energy,2), 'biomasa_ton': round(biom,2), 'R2': round(em.r2,3)})

st.subheader('Resultados')
st.dataframe(results, use_container_width=True)

# Alertas sencillas
ALERTA_TON = 20.0
alertas = [r for r in results if r['biomasa_ton'] >= ALERTA_TON]
if alertas:
    st.error(f'Alertas: {len(alertas)} instalaciones con biomasa semanal >= {ALERTA_TON} t')
else:
    st.success('Sin alertas de consumo elevado')

st.caption('Factor biomasa (t/MWh): {:.3f} basado en {} semanas coincidentes'.format(
    biomass_model.factor_ton_per_mwh, biomass_model.n_weeks
))
