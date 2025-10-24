from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime, date
import numpy as np

from .data_ingest import (
    load_hdd_series,
    load_energy_series,
    load_biomass_deliveries,
    to_daily_increments,
    series_to_map,
    group_by_week,
)
from pathlib import Path


@dataclass
class EnergyModel:
    slope: float
    intercept: float
    r2: float
    n: int


@dataclass
class BiomassModel:
    factor_ton_per_mwh: float  # tonnes per MWh
    n_weeks: int


def fit_linear(x: np.ndarray, y: np.ndarray) -> EnergyModel:
    if len(x) < 5:
        return EnergyModel(0.0, 0.0, 0.0, len(x))
    # Fit y = a x + b
    a, b = np.polyfit(x, y, 1)
    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 0.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    return EnergyModel(float(a), float(b), float(r2), int(len(x)))


def build_models(base_dir: Path) -> Tuple[Dict[str, EnergyModel], BiomassModel, Dict[str, float]]:
    # Load data
    hdd = load_hdd_series(base_dir / 'hdd-anual')
    hdd_map = {r.date.date(): r.hdd for r in hdd}

    energy_series = load_energy_series(base_dir / 'produccion-energetica')
    # Compute daily energy and fit per-install linear models vs HDD
    energy_models: Dict[str, EnergyModel] = {}
    all_pairs_x: List[float] = []
    all_pairs_y: List[float] = []
    energy_daily_by_inst: Dict[str, List[Tuple[datetime, float]]] = {}

    for inst, series in energy_series.items():
        daily = to_daily_increments(series)
        energy_daily_by_inst[inst] = daily
        x_vals: List[float] = []
        y_vals: List[float] = []
        for dt, inc in daily:
            h = hdd_map.get(dt.date())
            if h is None:
                continue
            x_vals.append(h)
            y_vals.append(inc)
        if len(x_vals) >= 10:
            model = fit_linear(np.array(x_vals), np.array(y_vals))
            energy_models[inst] = model
            all_pairs_x.extend(x_vals)
            all_pairs_y.extend(y_vals)

    # Global fallback model
    global_model = fit_linear(np.array(all_pairs_x), np.array(all_pairs_y)) if all_pairs_x else EnergyModel(0.0, 0.0, 0.0, 0)
    # Fill missing with global
    for inst in energy_series.keys():
        if inst not in energy_models:
            energy_models[inst] = global_model

    # Biomass factor: compute weekly deliveries vs weekly energy
    deliveries = load_biomass_deliveries(base_dir / 'consumo-biomasa.xlsx')
    deliveries_by_inst: Dict[str, List[Tuple[datetime, float]]] = {}
    for inst, dt, qty in deliveries:
        deliveries_by_inst.setdefault(inst, []).append((dt, qty))
    # weekly aggregates
    energy_weekly_by_inst: Dict[str, Dict[date, float]] = {
        inst: group_by_week(series) for inst, series in energy_daily_by_inst.items()
    }
    deliveries_weekly_by_inst: Dict[str, Dict[date, float]] = {
        inst: group_by_week(series) for inst, series in deliveries_by_inst.items()
    }

    ratios: List[float] = []
    for inst, eweeks in energy_weekly_by_inst.items():
        dweeks = deliveries_weekly_by_inst.get(inst, {})
        for wk, e_sum in eweeks.items():
            if e_sum <= 0:
                continue
            b_sum = dweeks.get(wk, 0.0)
            if b_sum <= 0:
                continue
            ratio = b_sum / e_sum  # tonnes per MWh
            # plausible filter
            if 0.05 <= ratio <= 0.8:
                ratios.append(ratio)

    if ratios:
        factor = float(np.median(ratios))
        n_weeks = len(ratios)
    else:
        factor = 0.2  # fallback ~ 1 tonne ~ 5 MWh
        n_weeks = 0

    biomass_model = BiomassModel(factor_ton_per_mwh=factor, n_weeks=n_weeks)

    # Baseline energy mean per installation (for non-heating days lower bound)
    baseline_energy: Dict[str, float] = {}
    for inst, series in energy_daily_by_inst.items():
        vals = [v for _, v in series if v > 0]
        baseline_energy[inst] = float(np.percentile(vals, 5)) if vals else 0.0

    return energy_models, biomass_model, baseline_energy


def predict_week_energy(hdd_next7: List[float], model: EnergyModel, baseline: float = 0.0) -> float:
    preds = [max(0.0, model.slope * h + model.intercept) for h in hdd_next7]
    # avoid negative predictions; clamp to baseline lower bound
    preds = [max(p, 0.0) for p in preds]
    return float(np.sum(preds))
