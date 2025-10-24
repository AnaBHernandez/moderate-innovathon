from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import os
import requests

AEMET_API_BASE = "https://opendata.aemet.es/opendata/api"
OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&daily=temperature_2m_mean&forecast_days=7&timezone=auto"
)


@dataclass
class ForecastDay:
    date: datetime
    tmean: float


def fetch_open_meteo(lat: float, lon: float) -> List[ForecastDay]:
    url = OPEN_METEO_URL.format(lat=lat, lon=lon)
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    dates = data.get('daily', {}).get('time', [])
    means = data.get('daily', {}).get('temperature_2m_mean', [])
    out: List[ForecastDay] = []
    for d, m in zip(dates, means):
        out.append(ForecastDay(date=datetime.fromisoformat(d), tmean=float(m)))
    return out


def fetch_aemet_daily_mean(lat: float, lon: float) -> Optional[List[ForecastDay]]:
    # Placeholder: AEMET forecast typically via municipality code, not lat/lon
    api_key = os.environ.get('AEMET_API_KEY')
    if not api_key:
        return None
    # Without municipality code, fallback to open-meteo
    return None


def get_forecast_next7(lat: float, lon: float) -> List[ForecastDay]:
    # Try AEMET, fallback to Open-Meteo
    aemet = fetch_aemet_daily_mean(lat, lon)
    if aemet:
        return aemet
    return fetch_open_meteo(lat, lon)


def hdd_from_tmean(tmean: float, base_temp: float = 18.0) -> float:
    return max(0.0, base_temp - float(tmean))


def compute_hdd_next7(lat: float, lon: float, base_temp: float = 18.0) -> List[float]:
    fc = get_forecast_next7(lat, lon)
    return [hdd_from_tmean(d.tmean, base_temp) for d in fc]
