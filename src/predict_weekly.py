from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from .modeling import build_models, predict_week_energy
from .aemet import compute_hdd_next7

BASE_DIR = Path('/workspace/datos_originales')
DEFAULT_LAT = 40.9701039
DEFAULT_LON = -5.6635397


def main():
    parser = argparse.ArgumentParser(description='Predicción semanal de consumo de biomasa')
    parser.add_argument('--inst', type=str, default='all', help='Códigos de instalación separados por coma o "all"')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT)
    parser.add_argument('--lon', type=float, default=DEFAULT_LON)
    parser.add_argument('--base-temp', type=float, default=18.0)
    parser.add_argument('--base-dir', type=str, default=str(BASE_DIR), help='Carpeta base con subdirs hdd-anual/, produccion-energetica/ y consumo-biomasa.xlsx')
    parser.add_argument('--out', type=str, default='/workspace/Entregables/prediccion_semanal.json')
    args = parser.parse_args()

    data_dir = Path(args.base_dir)
    energy_models, biomass_model, baseline_energy = build_models(data_dir)

    if args.inst.lower() != 'all':
        target_insts = set(s.strip().upper() for s in args.inst.split(','))
    else:
        target_insts = set(energy_models.keys())

    hdd7 = compute_hdd_next7(args.lat, args.lon, args.base_temp)

    results: List[Dict] = []
    for inst, model in energy_models.items():
        if inst not in target_insts:
            continue
        weekly_energy_mwh = predict_week_energy(hdd7, model, baseline_energy.get(inst, 0.0))
        weekly_biomass_ton = weekly_energy_mwh * biomass_model.factor_ton_per_mwh
        results.append({
            'instalacion': inst,
            'energia_semana_MWh': round(weekly_energy_mwh, 2),
            'biomasa_semana_ton': round(weekly_biomass_ton, 2),
            'modelo_r2': round(model.r2, 3),
        })

    output = {
        'fecha_generacion': datetime.utcnow().isoformat() + 'Z',
        'lat': args.lat,
        'lon': args.lon,
        'hdd_next7': hdd7,
        'biomass_factor_ton_per_MWh': biomass_model.factor_ton_per_mwh,
        'resultados': sorted(results, key=lambda x: x['instalacion'])
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
