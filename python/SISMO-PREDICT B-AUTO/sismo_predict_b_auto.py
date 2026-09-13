# -*- coding: utf-8 -*-
"""
SISMO-PREDICT B-AUTO
Núcleo estable de descarga, enriquecimiento y análisis sísmico.

Compatible con api.py para dashboard web.
No maneja puerto; el puerto se define en api.py / Uvicorn.
"""

import math
import re
import gzip
import io
import json  # <--- Asegúrate de que esté esta línea aquí
import requests
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone


# ============================================================
# Configuración
# ============================================================

USGS_EVENT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
DEFAULT_START = "1900-01-01"

MONTHS_ES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


# ============================================================
# Semilla histórica
# Coordenadas y profundidades aproximadas.
# ============================================================

SEED_EVENTS = [
    ("manual_colombia_2026", "2026-08-10T07:34:00", 5.50, -77.00, np.nan, 7.4, "Chocó, Colombia", "Colombia"),
    ("manual_venezuela_2026a", "2026-06-24T22:00:00", 10.50, -70.00, np.nan, 7.2, "Falla de Boconó, Venezuela", "Venezuela"),
    ("manual_venezuela_2026b", "2026-06-24T22:00:39", 10.55, -70.05, np.nan, 7.5, "Falla de Boconó, Venezuela", "Venezuela"),
    ("manual_turquia_2023a", "2023-02-06T04:17:00", 37.574, 36.920, np.nan, 7.8, "Kahramanmaraş, Turquía", "Turquía"),
    ("manual_turquia_2023b", "2023-02-06T13:24:00", 38.00, 37.00, np.nan, 7.5, "Kahramanmaraş, Turquía", "Turquía"),
    ("manual_japon_fukushima_2021a", "2021-02-13T23:07:00", 37.70, 141.60, np.nan, 7.1, "Fukushima, Japón", "Japón"),
    ("manual_japon_fukushima_2021b", "2021-02-13T23:07:20", 37.75, 141.65, np.nan, 7.0, "Fukushima, Japón", "Japón"),
    ("manual_mexico_2017", "2017-09-19T13:14:00", 18.50, -98.50, np.nan, 7.1, "Puebla/Morelos, México", "México"),
    ("manual_japon_tohoku_2011", "2011-03-11T14:46:00", 38.30, 142.40, 29.0, 9.1, "Tohoku, Japón", "Japón"),
    ("manual_indonesia_2007a", "2007-03-06T10:49:00", 0.50, 98.50, np.nan, 6.4, "Sumatra, Indonesia", "Indonesia"),
    ("manual_indonesia_2007b", "2007-03-06T12:49:00", 0.55, 98.55, np.nan, 6.3, "Sumatra, Indonesia", "Indonesia"),
    ("manual_pakistan_1997a", "1997-02-27T21:08:00", 30.20, 68.50, np.nan, 7.0, "Harnai, Pakistán", "Pakistán"),
    ("manual_pakistan_1997b", "1997-02-27T21:08:19", 30.25, 68.55, np.nan, 6.8, "Harnai, Pakistán", "Pakistán"),
    ("manual_china_1976a", "1976-07-27T03:42:00", 39.60, 118.20, np.nan, 7.6, "Tangshan, China", "China"),
    ("manual_china_1976b", "1976-07-27T18:45:00", 39.65, 118.25, np.nan, 7.1, "Tangshan, China", "China"),
    ("manual_chile_1960", "1960-05-22T15:11:00", -38.30, -73.00, np.nan, 9.5, "Valdivia, Chile", "Chile"),
    ("manual_bulgaria_1928a", "1928-04-14T11:00:00", 42.10, 26.50, np.nan, 6.8, "Chirpan, Bulgaria", "Bulgaria"),
    ("manual_bulgaria_1928b", "1928-04-18T21:20:00", 42.15, 26.55, np.nan, 7.1, "Chirpan, Bulgaria", "Bulgaria"),
    ("manual_ecuador_1868a", "1868-08-15T01:20:00", 0.30, -78.20, np.nan, 6.3, "Imbabura, Ecuador", "Ecuador"),
    ("manual_ecuador_1868b", "1868-08-16T02:00:00", 0.35, -78.25, np.nan, 6.7, "Imbabura, Ecuador", "Ecuador"),
]


# ============================================================
# FALLAS GEOLÓGICAS CONTINENTALES ACTIVAS
# ============================================================

FALLAS_GEOLOGICAS = [
    # (nombre, coordenadas [[lat, lon], ...], tipo, nivel_actividad)
    # América del Norte
    ("San Andrés", [[36.0, -120.5], [35.0, -119.0], [34.0, -118.0], [33.0, -116.5], [32.0, -115.0]], "transformante", "alta"),
    ("Hayward", [[37.8, -122.2], [37.5, -122.0], [37.2, -121.8]], "transformante", "alta"),
    ("Cascadia", [[48.5, -125.0], [46.0, -124.5], [43.0, -124.5], [40.5, -124.2]], "subducción", "alta"),
    
    # América Central y Caribe
    ("Motagua-Polochic", [[15.5, -89.5], [15.0, -90.0], [14.5, -90.5]], "transformante", "media"),
    ("Boconó", [[10.5, -70.0], [9.5, -70.5], [8.5, -71.0], [7.5, -71.5]], "transformante", "alta"),
    ("El Pilar", [[10.6, -63.0], [10.5, -64.0], [10.4, -65.0], [10.3, -66.0]], "transformante", "media"),
    
    # América del Sur
    ("Peru-Chile", [[-5.0, -81.0], [-15.0, -75.0], [-25.0, -70.5], [-35.0, -72.0], [-45.0, -74.0]], "subducción", "alta"),
  ("San Ramón", [
    [-33.32, -70.535],
    [-33.35, -70.540],
    [-33.39, -70.545],
    [-33.43, -70.550],
    [-33.47, -70.555],
    [-33.51, -70.560],
    [-33.55, -70.565],
    [-33.59, -70.570],
    [-33.62, -70.575]
], "inversa", "alta"),
    ("Liquiñe-Ofqui", [[-38.0, -72.5], [-40.0, -72.0], [-42.0, -72.5], [-44.0, -72.0]], "transformante", "media"),
    
    # Europa
    ("Anatolia Norte", [[40.7, 31.0], [40.5, 33.0], [40.3, 35.0], [40.0, 37.0], [39.5, 39.0]], "transformante", "alta"),
    ("Anatolia Este", [[38.0, 38.0], [37.5, 39.0], [37.0, 40.0]], "transformante", "alta"),
    ("Helenic", [[35.0, 24.0], [36.0, 26.0], [37.0, 28.0]], "subducción", "media"),
    
    # Asia
    ("Longmenshan", [[31.0, 103.5], [30.5, 104.0], [30.0, 104.5]], "inversa", "media"),
    ("Altyn Tagh", [[39.0, 88.0], [38.5, 92.0], [38.0, 96.0], [37.5, 100.0]], "transformante", "alta"),
    ("Kunlun", [[36.0, 90.0], [35.5, 95.0], [35.0, 100.0], [34.5, 105.0]], "transformante", "alta"),
    ("Japan Trench", [[40.0, 144.0], [38.0, 143.5], [36.0, 142.0], [34.0, 141.0]], "subducción", "alta"),
    ("Nankai", [[34.5, 138.0], [33.5, 136.0], [33.0, 134.0]], "subducción", "alta"),
    ("Sumatra", [[5.0, 95.0], [2.0, 97.0], [-1.0, 99.0], [-4.0, 101.0], [-7.0, 104.0]], "subducción", "alta"),
    
    # África
    ("East African Rift", [[12.0, 42.0], [8.0, 38.0], [4.0, 36.0], [0.0, 35.0], [-4.0, 34.0], [-8.0, 33.0]], "divergente", "media"),
    
    # Oceanía
    ("Alpine", [[-43.0, 170.5], [-43.5, 171.0], [-44.0, 171.5]], "transformante", "media"),
    ("Hikurangi", [[-38.0, 178.0], [-40.0, 177.0], [-42.0, 175.0]], "subducción", "alta"),
]

def calcular_radio_afectacion(magnitud, profundidad_km=10.0):
    """
    Calcula el radio aproximado de afectación sísmica en kilómetros.
    Basado en ecuaciones empíricas de atenuación.
    
    Args:
        magnitud: Magnitud del sismo (Mw)
        profundidad_km: Profundidad en km (default 10)
    
    Returns:
        Radio en km donde se siente el sismo
    """
    radio = 0.0
    
    if magnitud < 2.0:
        radio = 5.0
    elif magnitud < 4.0:
        radio = 10.0 + (magnitud - 2.0) * 15.0
    elif magnitud < 6.0:
        radio = 40.0 + (magnitud - 4.0) * 50.0
    elif magnitud < 7.0:
        radio = 140.0 + (magnitud - 6.0) * 150.0
    elif magnitud < 8.0:
        radio = 290.0 + (magnitud - 7.0) * 300.0
    else:
        radio = 590.0 + (magnitud - 8.0) * 500.0
    
    # Ajuste por profundidad (más profundo = mayor área pero menor intensidad)
    if profundidad_km > 100:
        radio = radio * 1.5
    elif profundidad_km > 50:
        radio = radio * 1.2
    
    return radio

# ============================================================
# Utilidades
# ============================================================

def fetch_json(url, timeout=60):
    """Fetch JSON genérico con User-Agent."""
    headers = {"User-Agent": "SismoPredict/1.0 (research)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"fetch_json error {url}: {e}")
    return None


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Distancia aproximada entre dos puntos geográficos en kilómetros.
    """
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except Exception:
        return np.nan

    R = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    )

    c = 2.0 * math.asin(math.sqrt(a))
    return R * c


def format_day_month(dt):
    """
    Formatea día y mes en español.
    """
    try:
        if pd.isna(dt):
            return ""
        dt = pd.Timestamp(dt)
        return f"{dt.day:02d} de {MONTHS_ES[dt.month]}"
    except Exception:
        return ""


def _is_one(value):
    """
    Devuelve True si el valor equivale a 1.
    """
    try:
        return float(value) == 1.0
    except Exception:
        return False


# ============================================================
# Descarga USGS[cite: 1, 2]
# ============================================================

def fetch_usgs_chunk(starttime, endtime, minmagnitude=6.0, limit=20000):
    """
    Descarga un bloque de eventos desde USGS[cite: 1, 2].
    """
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": minmagnitude,
        "orderby": "time",
        "limit": limit,
    }

    try:
        response = requests.get(USGS_EVENT_URL, params=params, timeout=180,verify=False)
    except Exception as e:
        print("Error de red consultando USGS[cite: 1, 2]:", e)
        return []

    if response.status_code in (204, 404):
        return []

    if not response.text:
        return []

    try:
        response.raise_for_status()
        data = response.json()
        return data.get("features", [])
    except Exception as e:
        print("Error parseando respuesta USGS[cite: 1, 2]:", e)
        return []


def fetch_usgs_range(start, end, minmagnitude=6.0, chunk_days=365):
    """
    Descarga eventos por bloques temporales.
    """
    try:
        current = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
    except Exception as e:
        print("Error convirtiendo fechas:", e)
        return []

    if current > end_dt:
        return []

    all_features = []

    while current <= end_dt:
        next_chunk = min(current + timedelta(days=chunk_days), end_dt + timedelta(days=1))

        print(
            f"Descargando USGS[cite: 1, 2]: {current.strftime('%Y-%m-%d')} -> "
            f"{next_chunk.strftime('%Y-%m-%d')} | M >= {minmagnitude}"
        )

        features = fetch_usgs_chunk(
            starttime=current.strftime("%Y-%m-%d"),
            endtime=next_chunk.strftime("%Y-%m-%d"),
            minmagnitude=minmagnitude,
        )

        all_features.extend(features)

        if len(features) >= 19999:
            print(
                "Advertencia: el bloque alcanzó el límite de USGS[cite: 1, 2]. "
                "Considere usar chunk_days más pequeño."
            )

        current = next_chunk

    return all_features


def parse_usgs_features(features):
    """
    Convierte features GeoJSON de USGS[cite: 1, 2] en DataFrame.
    """
    rows = []

    for feature in features:
        try:
            props = feature.get("properties", {}) or {}
            geom = feature.get("geometry", {}) or {}
            coords = geom.get("coordinates", []) or []

            if len(coords) < 2:
                continue

            lon = coords[0]
            lat = coords[1]
            depth = coords[2] if len(coords) > 2 else np.nan

            if lat is None or lon is None:
                continue

            raw_time = props.get("time")
            if raw_time is None:
                continue

            time_utc = pd.to_datetime(raw_time, unit="ms", utc=True)

            rows.append(
                {
                    "id": props.get("id"),
                    "time_utc": time_utc,
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "depth_km": depth,
                    "mag": props.get("mag"),
                    "mag_type": props.get("magType"),
                    "place": props.get("place"),
                    "tsunami": props.get("tsunami"),
                    "felt": props.get("felt"),
                    "cdi": props.get("cdi"),
                    "mmi": props.get("mmi"),
                    "alert": props.get("alert"),
                    "sig": props.get("sig"),
                    "url": props.get("url"),
                    "source": "usgs",
                }
            )

        except Exception as e:
            print("Error parseando feature USGS[cite: 1, 2]:", e)

    return pd.DataFrame(rows)


# ============================================================
# Semilla manual
# ============================================================

def load_manual_seed():
    """
    Carga eventos históricos manuales aproximados.
    """
    cols = [
        "id",
        "time_utc",
        "latitude",
        "longitude",
        "depth_km",
        "mag",
        "place",
        "country",
    ]

    df = pd.DataFrame(SEED_EVENTS, columns=cols)
    df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
    df["source"] = "manual_seed"
    df["mag_type"] = "historical"

    for col in ["tsunami", "felt", "cdi", "mmi", "alert", "sig", "url"]:
        df[col] = np.nan

    return df


# ============================================================
# Enriquecimiento
# ============================================================

def add_country(events):
    """
    Agrega país usando el campo place de USGS[cite: 1, 2].
    """
    if events.empty:
        return events

    events = events.copy()

    if "place" not in events.columns:
        events["place"] = ""

    if "country" not in events.columns:
        events["country"] = np.nan

    def parse_place(place):
        try:
            if isinstance(place, str) and "," in place:
                return place.split(",")[-1].strip()
        except Exception:
            pass
        return "Desconocido"

    events["country"] = events["country"].fillna(
        events["place"].apply(parse_place)
    ).fillna("Desconocido")

    events["country"] = events["country"].astype(str).str.strip()
    events.loc[events["country"].isin(["", "nan", "None"]), "country"] = "Desconocido"

    return events


def add_local_time(events):
    """
    Hora local aproximada usando longitud.
    No requiere librerías de zonas horarias.
    """
    if events.empty:
        return events

    events = events.copy()

    events["time_utc"] = pd.to_datetime(
        events["time_utc"],
        utc=True,
        errors="coerce",
    )

    local_times = []
    timezones = []

    for _, row in events.iterrows():
        try:
            if pd.isna(row["time_utc"]):
                local_times.append(pd.NaT)
                timezones.append("UTC")
                continue

            utc_dt = pd.Timestamp(row["time_utc"]).replace(tzinfo=None)

            if pd.notna(row["longitude"]):
                offset_hours = int(round(float(row["longitude"]) / 15.0))
            else:
                offset_hours = 0

            local_dt = utc_dt + timedelta(hours=offset_hours)

            local_times.append(local_dt)
            timezones.append(f"UTC{offset_hours:+d}")

        except Exception:
            local_times.append(pd.NaT)
            timezones.append("UTC")

    events["time_local"] = local_times
    events["timezone"] = timezones

    return events


# ============================================================
# Deduplicación
# ============================================================

def deduplicate_events(events, time_tol_min=10.0, dist_km=120.0, mag_tol=0.7):
    """
    Elimina eventos posiblemente duplicados.
    Conserva preferentemente USGS[cite: 1, 2] sobre semilla manual.
    """
    if events.empty:
        return events

    events = events.copy()

    events["time_utc"] = pd.to_datetime(
        events["time_utc"],
        utc=True,
        errors="coerce",
    )

    events = events.dropna(subset=["time_utc"]).reset_index(drop=True)

    if "source" not in events.columns:
        events["source"] = "usgs"

    events["source_rank"] = events["source"].map(
        {
            "usgs": 0,
            "manual_seed": 1,
        }
    ).fillna(2)

    events = events.sort_values(
        ["time_utc", "source_rank", "mag"],
        ascending=[True, True, False],
    ).reset_index(drop=True)

    keep_idx = []

    for i, row in events.iterrows():
        duplicated = False

        if (
            pd.notna(row["mag"])
            and pd.notna(row["latitude"])
            and pd.notna(row["longitude"])
        ):
            for j in reversed(keep_idx):
                kept = events.loc[j]

                if pd.isna(kept["time_utc"]):
                    continue

                dt_min = abs((row["time_utc"] - kept["time_utc"]).total_seconds()) / 60.0

                if dt_min > time_tol_min:
                    break

                if pd.isna(kept["mag"]):
                    continue

                if abs(float(row["mag"]) - float(kept["mag"])) > mag_tol:
                    continue

                d_km = haversine_km(
                    row["latitude"],
                    row["longitude"],
                    kept["latitude"],
                    kept["longitude"],
                )

                if pd.notna(d_km) and d_km <= dist_km:
                    duplicated = True
                    break

        if not duplicated:
            keep_idx.append(i)

    deduped = events.loc[keep_idx].drop(columns=["source_rank"]).reset_index(drop=True)

    return deduped

# ============================================================
# Detección de posibles dobletes
# ============================================================

def detect_doublets(
    events,
    max_hours=96.0,
    max_km=300.0,
    max_mag_diff=1.0,
    min_mag=6.0,
):
    """
    Marca posibles dobletes sísmicos.

    Regla simple:
    Dos eventos M >= min_mag, dentro de max_hours,
    a menos de max_km y con diferencia de magnitud <= max_mag_diff.
    """
    if events.empty:
        return events

    events = events.copy()

    events["time_utc"] = pd.to_datetime(
        events["time_utc"],
        utc=True,
        errors="coerce",
    )

    events = events.dropna(subset=["time_utc"]).sort_values("time_utc").reset_index(drop=True)

    if "id" not in events.columns or events["id"].isna().any():
        events["id"] = [f"evt_{i}" for i in range(len(events))]

    events["phenomenon_id"] = events["id"].astype(str)
    events["phenomenon_type"] = "Único"

    used = set()

    for i in range(len(events)):
        row_i = events.loc[i]

        if row_i["id"] in used:
            continue

        if pd.isna(row_i["mag"]) or float(row_i["mag"]) < min_mag:
            continue

        for j in range(i + 1, len(events)):
            row_j = events.loc[j]

            dt_hours = (
                row_j["time_utc"] - row_i["time_utc"]
            ).total_seconds() / 3600.0

            if dt_hours > max_hours:
                break

            if row_j["id"] in used:
                continue

            if pd.isna(row_j["mag"]) or float(row_j["mag"]) < min_mag:
                continue

            if abs(float(row_i["mag"]) - float(row_j["mag"])) > max_mag_diff:
                continue

            dist_km = haversine_km(
                row_i["latitude"],
                row_i["longitude"],
                row_j["latitude"],
                row_j["longitude"],
            )

            if pd.notna(dist_km) and dist_km <= max_km:
                group_id = f"DBT-{row_i['id']}"

                events.at[i, "phenomenon_id"] = group_id
                events.at[j, "phenomenon_id"] = group_id

                events.at[i, "phenomenon_type"] = "Doblete"
                events.at[j, "phenomenon_type"] = "Doblete"

                used.add(row_i["id"])
                used.add(row_j["id"])

                break

    return events


# ============================================================
# Impacto simple
# ============================================================

def add_event_impact(events):
    """
    Genera texto simple de impacto/comportamiento.
    """
    if events.empty:
        return events

    events = events.copy()

    def impact_text(row):
        impacts = []

        if _is_one(row.get("tsunami")):
            impacts.append("Alerta tsunami")

        alert_value = row.get("alert")
        if pd.notna(alert_value) and str(alert_value).strip() != "":
            impacts.append(f"PAGER {alert_value}")

        mmi_value = row.get("mmi")
        if pd.notna(mmi_value):
            impacts.append(f"MMI {mmi_value}")

        cdi_value = row.get("cdi")
        if pd.notna(cdi_value):
            impacts.append(f"CDI {cdi_value}")

        felt_value = row.get("felt")
        if pd.notna(felt_value):
            try:
                impacts.append(f"{int(felt_value)} reportes")
            except Exception:
                pass

        if row.get("phenomenon_type") == "Doblete":
            impacts.append("Posible doblete")

        if impacts:
            return "; ".join(impacts)

        return "Sin impacto reportado"

    events["impact"] = events.apply(impact_text, axis=1)

    return events


# ============================================================
# Tabla de fenómenos
# ============================================================

def build_phenomenon_table(events):
    """
    Agrupa eventos por fenómeno y arma tabla estilo cliente.
    """
    if events.empty:
        return pd.DataFrame()

    events = events.copy()

    if "phenomenon_id" not in events.columns:
        if "id" in events.columns:
            events["phenomenon_id"] = events["id"].astype(str)
        else:
            events["phenomenon_id"] = events.index.astype(str)

    rows = []

    for pid, group in events.groupby("phenomenon_id"):
        group = group.sort_values("time_utc")
        first = group.iloc[0]

        mags = sorted(
            [float(m) for m in group["mag"].dropna().tolist()],
            reverse=True,
        )

        if len(mags) > 1:
            mag_str = " y ".join([f"{m:.1f}" for m in mags])
        elif len(mags) == 1:
            mag_str = f"{mags[0]:.1f}"
        else:
            mag_str = ""

        phenomenon_type = (
            "Doblete Sísmico"
            if str(first.get("phenomenon_type", "")).strip() == "Doblete" and len(group) > 1
            else "Sismo Único Principal"
        )

        try:
            local_series = pd.to_datetime(group["time_local"], errors="coerce")
            local_times = [
                t.strftime("%H:%M") if pd.notna(t) else ""
                for t in local_series
            ]
        except Exception:
            local_times = []

        try:
            utc_series = pd.to_datetime(group["time_utc"], utc=True, errors="coerce")
            utc_times = [
                t.strftime("%H:%M") if pd.notna(t) else ""
                for t in utc_series
            ]
        except Exception:
            utc_times = []

        impacts = []

        if "tsunami" in group.columns:
            if group["tsunami"].apply(_is_one).any():
                impacts.append("Alerta tsunami")

        if "alert" in group.columns:
            if group["alert"].notna().any():
                pager_values = group["alert"].dropna().astype(str).unique()
                impacts.append("PAGER " + "/".join(pager_values))

        if "mmi" in group.columns:
            if group["mmi"].notna().any():
                impacts.append(f"MMI máx {group['mmi'].max()}")

        if "cdi" in group.columns:
            if group["cdi"].notna().any():
                impacts.append(f"CDI máx {group['cdi'].max()}")

        if phenomenon_type == "Doblete Sísmico":
            impacts.append("Detectado como posible doblete por tiempo/distancia")
        else:
            impacts.append("Evento principal")

        rows.append(
            {
                "País / Ubicación": first.get("country", "Desconocido"),
                "Lugar": first.get("place", ""),
                "Tipo de Fenómeno": phenomenon_type,
                "Año": first["time_utc"].year if pd.notna(first.get("time_utc")) else None,
                "Día y Mes": format_day_month(first.get("time_local")),
                "Hora Local / (UTC)": f"{' y '.join(local_times)} / ({' y '.join(utc_times)})",
                "Magnitud(es)": mag_str,
                "Magnitud Máxima": max(mags) if mags else np.nan,
                "Profundidad (km)": first.get("depth_km", np.nan),
                "Impacto / Comportamiento": "; ".join(impacts),
                "lat": first.get("latitude", np.nan),
                "lon": first.get("longitude", np.nan),
                "event_ids": ",".join(group["id"].astype(str).tolist()),
                "source": ",".join(group["source"].astype(str).unique().tolist()),
                "country": first.get("country", "Desconocido"),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values(["Año"], ascending=False).reset_index(drop=True)

    return df


# ============================================================
# Modelo probabilístico básico
# ============================================================

def estimate_b_value(magnitudes, mmin=6.0):
    """
    Estimación simple de valor b.
    Advertencia: requiere catálogo completo.
    """
    try:
        mags = np.asarray(
            [float(m) for m in magnitudes if pd.notna(m) and float(m) >= mmin],
            dtype=float,
        )
    except Exception:
        return np.nan

    if len(mags) < 10:
        return np.nan

    mean_m = mags.mean()
    denom = mean_m - mmin

    if denom <= 0:
        return np.nan

    beta = 1.0 / denom
    b = beta / np.log(10)

    return float(b)


def poisson_probability(rate_per_year, years):
    """
    Probabilidad Poissoniana de al menos un evento.
    """
    try:
        rate_per_year = float(rate_per_year)
        years = float(years)
    except Exception:
        return 0.0

    if rate_per_year <= 0:
        return 0.0

    return float(1.0 - np.exp(-rate_per_year * years))


def country_risk_table(phenomena, events, min_mag=6.0):
    """
    Tabla básica de riesgo por país.
    """
    if phenomena is None or phenomena.empty:
        return pd.DataFrame()

    if events is None or events.empty:
        return pd.DataFrame()

    phenomena = phenomena.copy()
    events = events.copy()

    if "country" not in phenomena.columns:
        if "País / Ubicación" in phenomena.columns:
            phenomena["country"] = phenomena["País / Ubicación"]
        else:
            phenomena["country"] = "Desconocido"

    phenomena["country"] = phenomena["country"].fillna("Desconocido")

    if "Magnitud Máxima" not in phenomena.columns:
        return pd.DataFrame()

    if "Tipo de Fenómeno" not in phenomena.columns:
        phenomena["Tipo de Fenómeno"] = "Sismo Único Principal"

    phenomena["Magnitud Máxima"] = pd.to_numeric(
        phenomena["Magnitud Máxima"],
        errors="coerce",
    )

    phenomena = phenomena[phenomena["Magnitud Máxima"] >= min_mag]

    if phenomena.empty:
        return pd.DataFrame()

    events["time_utc"] = pd.to_datetime(
        events["time_utc"],
        utc=True,
        errors="coerce",
    )

    valid_times = events["time_utc"].dropna()

    if valid_times.empty:
        return pd.DataFrame()

    start = valid_times.min()
    end = valid_times.max()

    years_span = max(1.0, float((end.year - start.year) + 1))

    risk = (
        phenomena.groupby("country")
        .agg(
            phenomena_count=("Magnitud Máxima", "size"),
            max_observed_mag=("Magnitud Máxima", "max"),
            doublet_count=(
                "Tipo de Fenómeno",
                lambda x: (x == "Doblete Sísmico").sum(),
            ),
        )
        .reset_index()
    )

    risk["years_span"] = years_span
    risk["annual_rate"] = risk["phenomena_count"] / years_span

    risk["prob_1y"] = risk["annual_rate"].apply(
        lambda r: poisson_probability(r, 1.0)
    )

    risk["prob_5y"] = risk["annual_rate"].apply(
        lambda r: poisson_probability(r, 5.0)
    )

    risk["prob_10y"] = risk["annual_rate"].apply(
        lambda r: poisson_probability(r, 10.0)
    )

    if "country" not in events.columns:
        events["country"] = "Desconocido"

    if "mag" not in events.columns:
        events["mag"] = np.nan

    global_b = estimate_b_value(events["mag"], mmin=min_mag)

    country_b = []

    for c in risk["country"]:
        country_mags = events[
            (events["country"] == c) & (events["mag"] >= min_mag)
        ]["mag"]

        b = estimate_b_value(country_mags, mmin=min_mag)

        if pd.isna(b) or b <= 0:
            b = global_b

        country_b.append(b)

    risk["b_value"] = country_b

    risk["mag_p10_exceedance"] = risk["b_value"].apply(
        lambda b: (min_mag + 1.0 / float(b)) if pd.notna(b) and float(b) > 0 else np.nan
    )

    risk = risk.sort_values("prob_10y", ascending=False).reset_index(drop=True)

    return risk


# ============================================================
# Pipeline simple para pruebas
# ============================================================

def run_pipeline(
    start=DEFAULT_START,
    end=None,
    minmag_fetch=6.0,
    minmag_model=6.0,
    include_seed=True,
):
    """
    Pipeline completo para probar el núcleo.
    No abre ningún puerto.
    """
    if end is None:
        end = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print("=" * 60)
    print("SISMO-PREDICT B-AUTO")
    print("=" * 60)

    features = fetch_usgs_range(
        start=start,
        end=end,
        minmagnitude=minmag_fetch,
        chunk_days=365,
    )

    events = parse_usgs_features(features)

    print(f"Eventos descargados desde USGS[cite: 1, 2]: {len(events)}")

    if include_seed:
        seed = load_manual_seed()
        print(f"Eventos históricos manuales incluidos: {len(seed)}")

        if events.empty:
            events = seed
        else:
            events = pd.concat([events, seed], ignore_index=True)

    if events.empty:
        print("No hay eventos para procesar.")
        return {
            "events": events,
            "phenomena": pd.DataFrame(),
            "risk": pd.DataFrame(),
        }

    events = deduplicate_events(events)
    print(f"Eventos después de deduplicación: {len(events)}")

    events = add_country(events)
    events = add_local_time(events)

    events["year"] = events["time_utc"].dt.year
    events["day_month"] = events["time_local"].apply(format_day_month)

    events = detect_doublets(
        events,
        max_hours=96.0,
        max_km=300.0,
        max_mag_diff=1.0,
        min_mag=minmag_model,
    )

    events = add_event_impact(events)

    phenomena = build_phenomenon_table(events)

    risk = country_risk_table(
        phenomena=phenomena,
        events=events,
        min_mag=minmag_model,
    )

    return {
        "events": events,
        "phenomena": phenomena,
        "risk": risk,
    }


# ============================================================
# MOTOR DE PREDICCIÓN Y ALERTAS
# ============================================================

VULNERABILITY_COUNTRY = {
    "Japón": 0.25, "Chile": 0.30, "México": 0.55, "Colombia": 0.50,
    "Ecuador": 0.55, "Perú": 0.55, "Indonesia": 0.60, "Turquía": 0.60,
    "Irán": 0.65, "Pakistán": 0.70, "China": 0.50, "EEUU": 0.30,
    "Estados Unidos": 0.30, "Italia": 0.45, "Grecia": 0.45,
    "Filipinas": 0.60, "Nueva Zelanda": 0.25, "Rusia": 0.40,
    "Venezuela": 0.55,
}
DEFAULT_VULNERABILITY = 0.50


def _country_depth_stats(events, country):
    try:
        d = events[
            (events["country"] == country) & (events["depth_km"].notna())
        ]["depth_km"].astype(float)
        if len(d) > 0:
            return (
                float(d.median()),
                float(d.quantile(0.25)),
                float(d.quantile(0.75)),
            )
    except Exception:
        pass
    return 30.0, 10.0, 60.0


def generate_forecasts(events, phenomena, risk, now=None):
    """
    Genera predicciones estadísticas con fecha estimada.
    """
    forecasts = []

    if events is None or events.empty:
        return forecasts
    if risk is None or risk.empty:
        return forecasts

    now = now or datetime.now(timezone.utc)
    ev = events.copy()
    ev["time_utc"] = pd.to_datetime(ev["time_utc"], utc=True, errors="coerce")

    # ------------------------------------------------------
    # 1) Predicción por recurrencia regional (por país)
    # ------------------------------------------------------
    for _, r in risk.iterrows():
        c = r.get("country")
        ce = ev[ev["country"] == c]
        if ce.empty:
            continue

        try:
            rate = float(r["annual_rate"])
        except Exception:
            rate = 0.0
        if rate <= 0:
            continue

        rec_days = 365.25 / rate
        last = ce["time_utc"].max()
        expected = last + pd.Timedelta(days=rec_days)
        overdue = expected < now

        base = now if overdue else expected
        window = max(15.0, rec_days * 0.5)

        p12 = 1 - math.exp(-rate * 1.0)

        mmax = float(r["max_observed_mag"]) if pd.notna(r.get("max_observed_mag")) else 7.0
        b = float(r["b_value"]) if pd.notna(r.get("b_value")) else 1.0
        if not (b > 0):
            b = 1.0

        m_p90 = min(9.5, 6.0 + 1.0 / b)
        mag_lo = round(max(6.0, mmax - 0.6), 1)
        mag_hi = round(max(mag_lo, min(9.5, max(m_p90, mmax))), 1)

        dmed, dq1, dq2 = _country_depth_stats(ev, c)

        vul = VULNERABILITY_COUNTRY.get(c, DEFAULT_VULNERABILITY)
        damage = min(1.0, p12 * (mmax / 9.5) * vul * 2)

        forecasts.append({
            "tipo": "Recurrencia regional",
            "country": c,
            "place": f"Zona sísmica de {c}",
            "fecha_estimada": base.isoformat(),
            "ventana_dias": int(window),
            "hora": "No determinable (prob. uniforme 24 h)",
            "mag_lo": mag_lo,
            "mag_hi": mag_hi,
            "profundidad_km": round(dmed),
            "prof_lo": round(dq1),
            "prof_hi": round(dq2),
            "probabilidad": round(p12, 3),
            "vencido": bool(overdue),
            "dano": "ALTO" if damage > 0.5 else "MEDIO" if damage > 0.25 else "BAJO",
            "confianza": "media" if len(ce) >= 5 else "baja",
        })

    # ------------------------------------------------------
    # 2) Predicción corto plazo por eventos recientes
    #    (réplica / doblete)
    # ------------------------------------------------------
    recent = ev[
        (ev["time_utc"] >= now - pd.Timedelta(days=30)) & (ev["mag"] >= 6.0)
    ]

    for _, e in recent.iterrows():
        try:
            mag = float(e["mag"])
        except Exception:
            continue

        delay = 3.0 if mag >= 6.5 else 7.0
        est = e["time_utc"] + pd.Timedelta(days=delay)
        if est < now:
            continue
        p = min(0.9, 0.08 + 0.06 * (mag - 6.0))

        depth = e.get("depth_km")

        forecasts.append({
            "tipo": "Réplica / doblete",
            "country": e.get("country", ""),
            "place": e.get("place", ""),
            "fecha_estimada": est.isoformat(),
            "ventana_dias": 3,
            "hora": "No determinable (prob. uniforme 24 h)",
            "mag_lo": round(max(4.5, mag - 1.2), 1),
            "mag_hi": round(mag - 0.2, 1),
            "profundidad_km": round(float(depth)) if pd.notna(depth) else None,
            "prof_lo": None,
            "prof_hi": None,
            "probabilidad": round(p, 3),
            "vencido": False,
            "dano": "MEDIO" if mag >= 7 else "BAJO",
            "confianza": "media",
        })

    forecasts.sort(key=lambda f: f["fecha_estimada"])
    return forecasts


def generate_alerts(events, forecasts, now=None):
    """
    Genera alertas automáticas.
    """
    alerts = []
    now = now or datetime.now(timezone.utc)

    if events is not None and not events.empty:
        ev = events.copy()
        ev["time_utc"] = pd.to_datetime(ev["time_utc"], utc=True, errors="coerce")
        rec = ev[ev["time_utc"] >= now - pd.Timedelta(hours=72)]

        for _, e in rec.iterrows():
            try:
                mag = float(e["mag"])
            except Exception:
                continue

            if mag >= 6.5:
                alerts.append({
                    "nivel": "ALTO",
                    "tipo": "Sismo principal reciente",
                    "country": e.get("country"),
                    "place": e.get("place"),
                    "mag": mag,
                    "fecha": e["time_utc"].isoformat(),
                    "mensaje": (
                        f"Sismo M{mag} en {e.get('place')}. "
                        "Vigilar réplicas/doblete durante 72 h."
                    ),
                })

        if "phenomenon_type" in rec.columns:
            # Corrección del filtrado para evitar UserWarning de Pandas
            db = rec[rec["phenomenon_type"] == "Doblete"]
            for _, e in db.iterrows():
                alerts.append({
                    "nivel": "ALTO",
                    "tipo": "Posible doblete sísmico",
                    "country": e.get("country"),
                    "place": e.get("place"),
                    "mag": e.get("mag"),
                    "fecha": e["time_utc"].isoformat(),
                    "mensaje": (
                        "Patrón de doblete detectado; "
                        "alta probabilidad de segundo evento."
                    ),
                })

    if forecasts:
        for f in forecasts:
            if f["tipo"] == "Réplica / doblete" and f["probabilidad"] >= 0.3:
                alerts.append({
                    "nivel": "MEDIO",
                    "tipo": "Predicción corto plazo",
                    "country": f["country"],
                    "place": f["place"],
                    "mag": f["mag_hi"],
                    "fecha": f["fecha_estimada"],
                    "mensaje": (
                        f"Prob. {int(f['probabilidad'] * 100)}% de réplica/doblete "
                        f"hasta M{f['mag_hi']}."
                    ),
                })

    return alerts


# ============================================================
# MOVIMIENTO DE PLACAS + SENSORES GEOFÍSICOS
# ============================================================

USGS_GEOMAG_URL = "https://geomag.usgs.gov/ws/data/"
GOES_XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
SWPC_KP_URL_SENSORS = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
SWPC_F107_URL = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"

PLATE_MOTION = [
    ("Nazca", -20, -70, 90, 7.0), ("Cocos", 10, -100, 45, 8.0),
    ("Caribe", 15, -70, 90, 2.0), ("Norteamérica", 40, -100, 250, 2.3),
    ("Pacífico", 30, -150, 300, 7.5), ("Juan de Fuca", 48, -128, 90, 4.0),
    ("Sudamérica", -30, -60, 270, 2.2), ("Eurasia", 50, 80, 90, 2.4),
    ("África", 10, 20, 45, 2.2), ("Arábiga", 25, 45, 10, 3.2),
    ("India", 20, 80, 10, 5.0), ("Australia", -25, 135, 10, 6.7),
    ("Filipinas", 25, 135, 315, 7.0), ("Antártica", -75, 0, 0, 1.0),
    ("Scotia", -57, -40, 90, 1.2),
]

OBSERVATORIES = [
    ("BOU", 40.14, -105.24, "Boulder, EEUU"),
    ("FRD", 38.20, -77.37, "Fredericksburg, EEUU"),
    ("FRN", 36.88, -119.73, "Fresno, EEUU"),
    ("TUC", 32.31, -110.71, "Tucson, EEUU"),
    ("CMO", 64.87, -147.86, "Alaska"),
    ("BRW", 71.32, -156.79, "Alaska"),
    ("SIT", 57.05, -135.33, "Alaska"),
    ("HON", 21.32, -158.00, "Hawái"),
    ("GUA", 13.59, 144.87, "Guam"),
    ("SJG", 18.11, -66.15, "Puerto Rico"),
    ("BSL", 30.37, -89.60, "Misisipi, EEUU"),
    ("NEW", 48.26, -117.12, "Washington, EEUU"),
]


def _fetch_json_simple(url, timeout=45):
    """Fetch JSON genérico con User-Agent para evitar bloqueos."""
    headers = {"User-Agent": "SismoPredict/1.0 (research)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"fetch_json_simple {url} -> {r.status_code}")
    except Exception as e:
        print(f"fetch_json_simple error {url}: {e}")
    return None


def _fetch_json_params(url, params, timeout=60):
    headers = {"User-Agent": "SismoPredict/1.0 (research)"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout,verify=False)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"fetch_json_params error {url}: {e}")
    return None


def _extract_number(value):
    """Extrae un número de un string como '1P', '2', 3.5, None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    # Quitar letras al final (ej: '1P' -> '1')
    m = re.match(r"^[+-]?\d*\.?\d+", s)
    if m:
        try:
            return float(m.group(0))
        except Exception:
            return None
    return None


def _extract_usgs_series(data, element):
    """
    Extrae serie de valores desde estructura USGS[cite: 1, 2] geomag.
    Estructura típica: {"type":..., "metadata":..., "times":[...],
                        "values": {"BOU_H": [...], ...}}
    """
    vals = []
    if not isinstance(data, dict):
        return vals

    values = data.get("values")
    if not values:
        return vals

    # values puede ser dict {clave: [lista_valores]}
    if isinstance(values, dict):
        for key, arr in values.items():
            # clave tipo "BOU_H" -> buscar la que termine con el elemento
            if key.upper().endswith(f"_{element.upper()}"):
                if isinstance(arr, list):
                    for v in arr:
                        n = _extract_number(v)
                        if n is not None:
                            vals.append(n)
                break
    # values puede ser lista de listas
    elif isinstance(values, list):
        for row in values:
            if isinstance(row, list) and row:
                # primer valor numérico
                for v in row:
                    n = _extract_number(v)
                    if n is not None:
                        vals.append(n)
                        break
    return vals


def _status_dev(dev, thr):
    if dev is None:
        return "SIN DATOS", "gray"
    if dev > thr:
        return "ALTO", "red"
    if dev < -thr:
        return "BAJO", "blue"
    return "NORMAL", "green"


def _nearest_obs(lat, lon):
    best = None
    bd = 1e18
    for code, la, lo, name in OBSERVATORIES:
        d = haversine_km(lat, lon, la, lo)
        if pd.notna(d) and d < bd:
            bd = d
            best = (code, name, d)
    return best

def fetch_multisensor(lat, lon, events=None):
    """
    Panel multi-sensor alrededor del último sismo.
    """
    sensors = []
    note = ("Fuentes: USGS[cite: 1, 2] geomagnetismo (magnetómetro y campo eléctrico), "
            "NOAA SWPC (Kp, F10.7, X-ray). "
            "Infrasonido e InSAR no tienen API pública gratuita.")

    obs = _nearest_obs(lat, lon) if (lat is not None and lon is not None
                                      and pd.notna(lat) and pd.notna(lon)) else None

    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # ========================================================
    # 1) CAMPO MAGNÉTICO (H) desde observatorio USGS[cite: 1, 2] cercano
    # ========================================================
    if obs:
        code, name, dist = obs
        data = _fetch_json_params(USGS_GEOMAG_URL, {
            "id": code, "format": "json", "elements": "H",
            "starttime": start, "endtime": end, "sampling_period": 3600
        })
        series = _extract_usgs_series(data, "H")
        if len(series) > 3:
            base = float(np.median(series))
            dev = series[-1] - base
            st, col = _status_dev(dev, 40)
            sensors.append({
                "name": f"Campo magnético (H)",
                "value": round(dev, 1),
                "unit": "nT",
                "status": st,
                "color": col,
                "source": f"USGS[cite: 1, 2] {code} ({int(dist)} km)"
            })
        else:
            sensors.append({
                "name": f"Campo magnético (H)",
                "value": None, "unit": "nT",
                "status": "SIN DATOS", "color": "gray",
                "source": f"USGS[cite: 1, 2] {code}"
            })

        # ====================================================
        # 2) CAMPO ELÉCTRICO / CORRIENTES TELÚRICAS (E-E)
        # ====================================================
        edata = _fetch_json_params(USGS_GEOMAG_URL, {
            "id": code, "format": "json", "elements": "E-E",
            "starttime": start, "endtime": end, "sampling_period": 3600
        })
        ee = _extract_usgs_series(edata, "E-E")
        if len(ee) > 3:
            base = float(np.median(ee))
            dev = ee[-1] - base
            st, col = _status_dev(dev, 2)
            sensors.append({
                "name": "Corrientes telúricas (E-E)",
                "value": round(dev, 2),
                "unit": "mV/km",
                "status": st,
                "color": col,
                "source": f"USGS[cite: 1, 2] {code}"
            })

    # ========================================================
    # 3) ÍNDICE KP (NOAA SWPC)
    # ========================================================
    kp_data = _fetch_json_simple(SWPC_KP_URL_SENSORS)
    if isinstance(kp_data, list) and kp_data:
        try:
            val = _extract_number(kp_data[-1].get("kp"))
            if val is not None:
                st, col = _status_dev(val - 2, 2)
                sensors.append({
                    "name": "Índice Kp",
                    "value": val,
                    "unit": "",
                    "status": st,
                    "color": col,
                    "source": "NOAA SWPC"
                })
        except Exception as e:
            print("Kp parse error:", e)

    # ========================================================
    # 4) RADIOFRECUENCIA F10.7
    # ========================================================
    f107 = _fetch_json_simple(SWPC_F107_URL)
    if isinstance(f107, list) and f107:
        try:
            last = f107[-1]
            val = None
            for k in ("flux", "f107", "observed"):
                v = last.get(k)
                val = _extract_number(v)
                if val is not None:
                    break
            if val is not None:
                st = "ALTO" if val > 200 else "BAJO" if val < 70 else "NORMAL"
                col = "red" if st == "ALTO" else "blue" if st == "BAJO" else "green"
                sensors.append({
                    "name": "Radiofrecuencia (F10.7)",
                    "value": round(val, 1),
                    "unit": "sfu",
                    "status": st,
                    "color": col,
                    "source": "NOAA SWPC"
                })
        except Exception as e:
            print("F10.7 parse error:", e)

    # ========================================================
    # 5) IONÓSFERA (GOES X-ray) — URL corregida
    # ========================================================
    xray = _fetch_json_simple(GOES_XRAY_URL)
    if isinstance(xray, list) and xray:
        try:
            val = _extract_number(xray[-1].get("short_flux") or xray[-1].get("flux"))
            if val is not None:
                st = "ALTO" if val > 1e-5 else "BAJO" if val < 1e-8 else "NORMAL"
                col = "red" if st == "ALTO" else "blue" if st == "BAJO" else "green"
                sensors.append({
                    "name": "Ionósfera (X-ray GOES)",
                    "value": f"{val:.1e}",
                    "unit": "W/m²",
                    "status": st,
                    "color": col,
                    "source": "NOAA GOES"
                })
        except Exception as e:
            print("X-ray parse error:", e)

    # ========================================================
    # 6) Actividad sísmica (ratio 7d vs base)
    # ========================================================
    if events is not None and not events.empty:
        try:
            ev = events.copy()
            ev["time_utc"] = pd.to_datetime(ev["time_utc"], utc=True, errors="coerce")
            ev = ev.dropna(subset=["time_utc"])
            if not ev.empty:
                span_days = max(1.0, (ev.time_utc.max() - ev.time_utc.min()).days)
                weekly_base = len(ev) / (span_days / 7.0) if span_days > 0 else 1.0
                recent = ev[ev.time_utc >= now - pd.Timedelta(days=7)]
                ratio = (len(recent) / weekly_base) if weekly_base > 0 else 1.0
                st = "ALTO" if ratio > 1.5 else "BAJO" if ratio < 0.5 else "NORMAL"
                col = "red" if st == "ALTO" else "blue" if st == "BAJO" else "green"
                sensors.append({
                    "name": "Actividad sísmica (7d)",
                    "value": round(ratio, 2),
                    "unit": "x base",
                    "status": st,
                    "color": col,
                    "source": "USGS[cite: 1, 2] catálogo"
                })
        except Exception as e:
            print("Actividad sísmica error:", e)

    # ========================================================
    # 7) Sensores no disponibles públicamente
    # ========================================================
    sensors.append({
        "name": "Infrasonido",
        "value": None, "unit": "",
        "status": "SIN API", "color": "gray",
        "source": "requiere estación local"
    })
    sensors.append({
        "name": "Deformación GPS/InSAR",
        "value": None, "unit": "",
        "status": "SIN API", "color": "gray",
        "source": "requiere procesamiento"
    })

    return {
        "observatory": (obs[0] if obs else None),
        "sensors": sensors,
        "note": note
    }


# ============================================================
# MÓDULO CIELO (satélites + asteroides) Y SUBSUELO
# ============================================================

ISS_URL = "https://api.wheretheiss.at/v1/satellites/25544"
CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"
CELESTRAK_GROUPS = ["stations", "weather", "gps-ops"]
NEOWS_URL = "https://api.nasa.gov/neo/rest/v1/feed"
NASA_KEY = "DEMO_KEY"

CRUST1_MOHO_URLS = [
    "https://igppweb.ucsd.edu/~gabi/crust1/down/mohd.xyz.gz",
    "https://igppweb.ucsd.edu/~gabi/crust1/down/moho.xyz.gz",
]

_MOHO_GRID = None


# ---------- CIELO ----------

def fetch_iss():
    data = fetch_json(ISS_URL)
    if isinstance(data, dict):
        return {
            "name": "ISS",
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "altitude_km": data.get("altitude"),
            "velocity_kmh": data.get("velocity"),
            "visibility": data.get("visibility"),
        }
    return None


def _parse_tle(text):
    lines = [l.rstrip("\n") for l in text.splitlines()]
    sats = []
    pending = None
    for i, l in enumerate(lines):
        s = l.strip()
        if not s:
            continue
        if s.startswith("1 "):
            name = pending or "SAT"
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("2 "):
                sats.append({"name": name, "l1": s, "l2": lines[i + 1].strip()})
        elif not s.startswith("2 "):
            pending = s
    return sats


def _teme_to_llh(r, gmst):
    x, y, z = r
    cg = math.cos(gmst); sg = math.sin(gmst)
    xp = cg * x + sg * y
    yp = -sg * x + cg * y
    zp = z
    lon = math.degrees(math.atan2(yp, xp))
    rxy = math.sqrt(xp * xp + yp * yp)
    lat = math.degrees(math.atan2(zp, rxy))
    alt = math.sqrt(xp * xp + yp * yp + zp * zp) - 6371.0
    return lat, lon, alt


# ---------- CLASIFICACIÓN DE SATÉLITES ----------

SPACE_TRACK_USER = ""   # opcional: cuenta gratuita en space-track.org
SPACE_TRACK_PASS = ""   # si la llenas, desbloquea TODO el catálogo (incl. militar)

CELESTRAK_GROUPS = ["stations", "weather", "gps-ops", "glonass-ops",
                    "galileo", "beidou", "science", "military"]

# (prefijo, país, bandera, militar) — heurística pública
SAT_CLASS = [
    ("USA", "EEUU", "🇺🇸", True), ("NROL", "EEUU", "🇺", True),
    ("DMSP", "EEUU", "🇺", True), ("SBIRS", "EEUU", "🇺", True), ("DSP", "EEUU", "🇺🇸", True),
    ("NAVSTAR", "EEUU", "🇺🇸", False), ("GPS", "EEUU", "🇺", False),
    ("GOES", "EEUU", "🇺", False), ("NOAA", "EEUU", "🇺🇸", False),
    ("STARLINK", "EEUU", "🇺🇸", False), ("LANDSAT", "EEUU", "🇺🇸", False),
    ("HUBBLE", "EEUU", "🇺", False), ("ISS", "Internacional", "🌐", False),
    ("COSMOS", "Rusia", "🇷", True), ("GLONASS", "Rusia", "🇷🇺", False),
    ("METEOR", "Rusia", "🇷🇺", False), ("SOYUZ", "Rusia", "🇷🇺", False),
    ("PROGRESS", "Rusia", "🇷🇺", False),
    ("YAOGAN", "China", "🇨🇳", True), ("BEIDOU", "China", "🇨🇳", False),
    ("GAOFEN", "China", "🇨", False), ("FENGYUN", "China", "🇨🇳", False),
    ("TIANGONG", "China", "🇨🇳", False),
    ("GALILEO", "UE", "🇪", False), ("SENTINEL", "UE", "🇪🇺", False), ("METOP", "UE", "🇪", False),
    ("COSMO-SKYMED", "Italia", "🇮🇹", True), ("PAZ", "España", "🇪🇸", True),
    ("SEOSAT", "España", "🇪🇸", False),
    ("HIMAWARI", "Japón", "🇯🇵", False), ("ALOS", "Japón", "🇯🇵", False), ("QZS", "Japón", "🇯", False),
    ("RISAT", "India", "🇮", True), ("CARTOSAT", "India", "🇮", False), ("GSAT", "India", "🇮🇳", False),
    ("ONEWEB", "Reino Unido", "🇬", False), ("SKYNET", "Reino Unido", "🇬🇧", True),
    ("EROS", "Israel", "🇮", True), ("OFEK", "Israel", "🇮🇱", True),
    ("TERRASAR", "Alemania", "🇩🇪", True), ("TANDEM", "Alemania", "🇩🇪", True),
    ("PLEIADES", "Francia", "🇫🇷", True), ("SPOT", "Francia", "🇫🇷", False),
    ("RADARSAT", "Canadá", "🇨🇦", False), ("KOMPSAT", "Corea del Sur", "🇰🇷", False),
]

def classify_sat(name):
    n = (name or "").upper()
    for pref, country, flag, mil in SAT_CLASS:
        if n.startswith(pref):
            return country, flag, mil
    return "—", "🌐", False

DEBRIS_GROUPS = ["cosmos-2251-deb", "iridium-33-deb", "fengyun-1c-deb"]

def _parse_bstar(s):
    try:
        sign = -1 if s[0] == "-" else 1
        mant = float(s[1:6]) / 1e5
        exp = int(s[6:8].replace("-", "-"))
        return sign * mant * (10 ** exp)
    except Exception:
        return 0.0

def _tle_orbit_params(l1, l2):
    try:
        e = float("0." + l2[26:33].strip())
        n = float(l2[52:63].strip())
        bstar = _parse_bstar(l1[60:68])
        T = 86400.0 / n
        a = (398600.4418 * (T / (2 * math.pi)) ** 2) ** (1.0 / 3.0)
        return e, n, bstar, a * (1 - e) - 6371.0
    except Exception:
        return None, None, 0.0, None

def _fetch_tle_group(group):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SismoPredict/1.0"}
    if group == "military":
        try:
            r = requests.get("https://www.prismnet.com/~mmccants/tles/classified.tle",
                             headers=headers, timeout=60,verify=False)
            if r.status_code == 200 and r.text.strip():
                return _parse_tle(r.text)
        except Exception:
            pass
        return []
    for base in ("https://celestrak.org/NORAD/elements/gp.php",
                 "https://celestrak.com/NORAD/elements/gp.php"):
        try:
            r = requests.get(base, params={"GROUP": group, "FORMAT": "tle"},
                             headers=headers, timeout=60,verify=False)
            if r.status_code == 200 and r.text.strip():
                return _parse_tle(r.text)
        except Exception:
            continue
    return []


def _fetch_spacetrack():
    if not (SPACE_TRACK_USER and SPACE_TRACK_PASS):
        return []
    try:
        s = requests.Session()
        r = s.post("https://www.space-track.org/ajaxauth/login",
                   data={"identity": SPACE_TRACK_USER, "password": SPACE_TRACK_PASS}, timeout=30)
        if r.status_code != 200:
            return []
        r2 = s.get("https://www.space-track.org/basicspacedata/query/class/tle_latest/"
                   "EPOCH/%3Enow-14/format/3le", timeout=90)
        if r2.status_code == 200:
            return _parse_tle(r2.text)[:400]
    except Exception as e:
        print("space-track error:", e)
    return []


_TLE_CACHE = {"ts": None, "sats": []}

# Variables globales para detección de reentradas (CORREGIDO: definidas antes de usarse)
_PREV_CAT = {"names": None}
_REENTRIES = []

def fetch_satellites(max_per_group=30, max_age_s=3600):
    out = []
    try:
        from sgp4.api import Satrec, jday, gstime
    except Exception:
        try:
            from sgp4.api import Satrec, jday
            from sgp4.ext import gstime
        except Exception:
            return out

    now = datetime.now(timezone.utc)

    if (_TLE_CACHE["ts"] is not None and _TLE_CACHE["sats"]
            and (now - _TLE_CACHE["ts"]).total_seconds() < max_age_s):
        tle_sats = _TLE_CACHE["sats"]
    else:
        tle_sats = _fetch_spacetrack()
        if not tle_sats:
            for group in CELESTRAK_GROUPS:
                tle_sats.extend(_fetch_tle_group(group)[:max_per_group])
        if tle_sats:
            _TLE_CACHE["ts"] = now
            _TLE_CACHE["sats"] = tle_sats
        else:
            tle_sats = _TLE_CACHE["sats"]

    jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second)
    gm = gstime(jd + fr)

    for s in tle_sats:
        try:
            e, n, bstar, perigee = _tle_orbit_params(s["l1"], s["l2"])
            sat = Satrec.twoline2rv(s["l1"], s["l2"])
            err, r, v = sat.sgp4(jd, fr)
            if err != 0:
                continue
            lat, lon, alt = _teme_to_llh(r, gm)
            country, flag, mil = classify_sat(s["name"])
            name_up = (s["name"] or "").upper()
            is_deb = " DEB" in name_up
            decaying = perigee is not None and perigee < 220
            trail = []
            for dt in (-0.03125, 0.0, 0.03125):
                ee, rr, vv = sat.sgp4(jd, fr + dt)
                if ee == 0:
                    la2, lo2, _ = _teme_to_llh(rr, gm)
                    trail.append([la2, lo2])
            out.append({"name": s["name"], "latitude": lat, "longitude": lon,
                        "altitude_km": alt, "country": country, "flag": flag,
                        "military": mil, "type": "deb" if is_deb else "sat",
                        "decaying": decaying, "perigee_km": perigee, "trail": trail})
        except Exception:
            pass

    # CORREGIDO: bloque de reentradas FUERA del bucle for (indentación correcta)
    names = set(x["name"] for x in out)
    global _PREV_CAT, _REENTRIES
    if _PREV_CAT["names"] is not None:
        for g in list(_PREV_CAT["names"] - names)[:10]:
            _REENTRIES.insert(0, {"name": g, "ts": now.isoformat()})
        del _REENTRIES[20:]
    _PREV_CAT["names"] = names
    return out

def get_reentries():
    return _REENTRIES


# ---------- LANZAMIENTOS (referencia de actividad) ----------

_LAUNCH_CACHE = {"ts": None, "data": []}

def fetch_launches(max_age_s=900):
    now = datetime.now(timezone.utc)
    if (_LAUNCH_CACHE["ts"] is not None and _LAUNCH_CACHE["data"]
            and (now - _LAUNCH_CACHE["ts"]).total_seconds() < max_age_s):
        return _LAUNCH_CACHE["data"]
    out = []
    for path in ("previous", "upcoming"):
        try:
            data = fetch_json(f"https://ll.thespacedevs.com/2.2.0/launch/{path}/?limit=5", timeout=30)
            if isinstance(data, dict):
                for l in data.get("results", []):
                    pad = l.get("pad") or {}
                    out.append({
                        "name": l.get("name"),
                        "status": (l.get("status") or {}).get("name"),
                        "net": l.get("net"),
                        "lat": pad.get("latitude"),
                        "lon": pad.get("longitude"),
                        "type": path,
                    })
        except Exception:
            continue
    if out:
        _LAUNCH_CACHE["ts"] = now
        _LAUNCH_CACHE["data"] = out
    return out

def fetch_asteroids(days=7):
    now = datetime.now(timezone.utc)
    start = now.strftime("%Y-%m-%d")
    end = (now + timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"{NEOWS_URL}?start_date={start}&end_date={end}&api_key={NASA_KEY}"
    data = fetch_json(url)
    out = []
    if isinstance(data, dict):
        for date_key, lst in (data.get("near_earth_objects") or {}).items():
            for o in lst or []:
                try:
                    ca = (o.get("close_approach_data") or [{}])[0]
                    dm = o.get("estimated_diameter", {}).get("meters", {})
                    out.append({
                        "name": o.get("name"),
                        "date": date_key,
                        "distance_km": float(ca.get("miss_distance", {}).get("kilometers", 0)),
                        "velocity_kmh": float(ca.get("relative_velocity", {}).get("kilometers_per_hour", 0)),
                        "diameter_m": (float(dm.get("estimated_diameter_min", 0)) +
                                       float(dm.get("estimated_diameter_max", 0))) / 2,
                        "hazardous": bool(o.get("is_potentially_hazardous_asteroid")),
                    })
                except Exception:
                    pass
    out.sort(key=lambda a: a["distance_km"])
    return out[:20]


# ---------- SUBSUELO ----------

def _load_moho_grid():
    global _MOHO_GRID
    if _MOHO_GRID is not None:
        return _MOHO_GRID
    for url in CRUST1_MOHO_URLS:
        try:
            r = requests.get(url, timeout=90)
            if r.status_code != 200:
                continue
            raw = gzip.open(io.BytesIO(r.content)).read().decode()
            grid = {}
            for line in raw.splitlines():
                p = line.split()
                if len(p) >= 3:
                    lon, lat, val = float(p[0]), float(p[1]), float(p[2])
                    grid[(round(lon), round(lat))] = val
            if grid:
                _MOHO_GRID = grid
                return grid
        except Exception:
            continue
    _MOHO_GRID = {}
    return _MOHO_GRID


def _moho_at(lat, lon):
    if lat is None or lon is None:
        return None
    grid = _load_moho_grid()
    if not grid:
        return None
    return grid.get((round(float(lon)), round(float(lat))))


def build_subsurface(events, lat=None, lon=None):
    out = {"cross_section": [], "moho_km": None,
           "note": "Corte construido con hipocentros reales (USGS[cite: 1, 2]). Moho según CRUST1.0."}
    if events is not None and not events.empty:
        ev = events.copy()
        ev["depth_km"] = pd.to_numeric(ev["depth_km"], errors="coerce")
        ev = ev.dropna(subset=["depth_km", "latitude", "longitude"])
        for _, r in ev.tail(400).iterrows():
            out["cross_section"].append({
                "lat": float(r.latitude), "lon": float(r.longitude),
                "depth_km": float(r.depth_km),
                "mag": float(r.mag) if pd.notna(r.get("mag")) else None,
            })
    out["moho_km"] = _moho_at(lat, lon)
    return out


# ============================================================
# CLIMA ESPACIAL, SISTEMA SOLAR, SENTRY, OZONO
# ============================================================

SWPC_MAG_URL = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json"

ORBIT_OBJECTS = ["C/2023 A3", "12P/Pons-Brooks", "2005 EG94", "2019 LR4",
                 "2004 TF10", "2019 QC4", "2018 QT1", "2014 CE"]

_SPACE_CACHE = {"ts": None, "orbits": []}


def fetch_spaceweather():
    out = {"kp": None, "xray": None, "f107": None, "bz": None, "bt": None,
           "wind_speed": None, "level": "NORMAL"}
    kp = _fetch_json_simple(SWPC_KP_URL_SENSORS)
    if isinstance(kp, list) and kp:
        out["kp"] = _extract_number(kp[-1].get("kp"))
    xr = _fetch_json_simple(GOES_XRAY_URL)
    if isinstance(xr, list) and xr:
        out["xray"] = _extract_number(xr[-1].get("short_flux") or xr[-1].get("flux"))
    f = _fetch_json_simple(SWPC_F107_URL)
    if isinstance(f, list) and f:
        out["f107"] = _extract_number(f[-1].get("flux"))
    mg = _fetch_json_simple(SWPC_MAG_URL)
    if isinstance(mg, list) and mg:
        out["bz"] = _extract_number(mg[-1].get("Bz"))
        out["bt"] = _extract_number(mg[-1].get("Bt"))
    for url in ("https://services.swpc.noaa.gov/json/ace_realtime_solar_wind_1-day.json",
                "https://services.swpc.noaa.gov/json/rtsw/solar_wind_1-day.json"):
        sw = _fetch_json_simple(url)
        if isinstance(sw, list) and sw:
            out["wind_speed"] = _extract_number(sw[-1].get("speed"))
            break
    k = out["kp"] or 0
    out["level"] = ("TORMENTA" if (k >= 5 or (out["xray"] or 0) > 1e-5)
                    else "ACTIVO" if k >= 4 else "NORMAL")
    return out


def fetch_sentry():
    data = _fetch_json_simple("https://ssd-api.jpl.nasa.gov/sentry.api?format=json")
    out = []
    if isinstance(data, dict) and "data" in data:
        fields = data.get("fields", [])
        for row in data.get("data", [])[:10]:
            rec = dict(zip(fields, row))
            out.append({
                "name": rec.get("fullname") or rec.get("des") or rec.get("name"),
                "ps": rec.get("ps"),
                "diameter": rec.get("diameter"),
                "h": rec.get("h"),
            })
    return out


def _parse_horizons(txt):
    pts, in_block = [], False
    for line in txt.splitlines():
        if "$$SOE" in line:
            in_block = True
            continue
        if "$$EOE" in line:
            break
        if in_block:
            p = line.split()
            if len(p) >= 6:
                try:
                    pts.append([float(p[1]), float(p[2]), float(p[4]), float(p[5])])
                except Exception:
                    pass
    return pts


def fetch_orbits(max_age_s=900):
    now = datetime.now(timezone.utc)
    if (_SPACE_CACHE["ts"] is not None and _SPACE_CACHE["orbits"]
            and (now - _SPACE_CACHE["ts"]).total_seconds() < max_age_s):
        return _SPACE_CACHE["orbits"]
    start = (now - timedelta(days=45)).strftime("%Y-%m-%d")
    stop = (now + timedelta(days=45)).strftime("%Y-%m-%d")
    out = []
    for name in ORBIT_OBJECTS:
        try:
            params = {"format": "json", "COMMAND": f"'{name}'", "OBJ_DATA": "NO",
                      "MAKE_EPHEM": "YES", "EPHEM_TYPE": "VECTORS", "CENTER": "'500@10'",
                      "START_TIME": f"'{start}'", "STOP_TIME": f"'{stop}'",
                      "STEP_SIZE": "'5 d'", "VEC_TABLE": "3"}
            r = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api",
                             params=params, timeout=30,verify=False)
            if r.status_code != 200:
                continue
            pts = _parse_horizons((r.json() or {}).get("result", ""))
            if pts:
                out.append({"name": name, "points": pts})
        except Exception:
            continue
    if out:
        _SPACE_CACHE["ts"] = now
        _SPACE_CACHE["orbits"] = out
    return out


def fetch_ozone():
    for url in ("https://ozonewatch.gsfc.nasa.gov/Data/merra2/GSFC_MERRA2_1979_present_sat_merged_area.txt",
                "https://ozonewatch.gsfc.nasa.gov/Data/TOMS_OMI_area.txt"):
        try:
            r = requests.get(url, timeout=30,verify=False)
            if r.status_code != 200:
                continue
            lines = [l for l in r.text.splitlines() if l.strip()]
            for l in reversed(lines):
                p = l.replace(",", " ").split()
                nums = [float(x) for x in p if _extract_number(x) is not None]
                if nums:
                    return {"area_mkm2": nums[-1], "source": "NASA Ozone Watch"}
        except Exception:
            continue
    return None


# ============================================================
# BASE DE DATOS DE FALLAS ACTIVAS (GEM + USGS + Chile + embebidas)
# ============================================================

import os as _os
import time as _time

GEM_FAULTS_URL = ("https://raw.githubusercontent.com/GEMScienceTools/"
                  "gem-global-active-faults/master/geojson/gem_active_faults.geojson")
USGS_FAULTS_URL = ("https://services.arcgis.com/v01gqwM5QqNysAAi/ArcGIS/rest/services/"
                   "USGS_Quaternary_Fault_and_Fold_Database/FeatureServer/0/query")
CHILE_FAULTS_CANDIDATES = [
    "https://fallasactivas.cl/geojson/fallas.geojson",
    "https://fallasactivas.cl/data/fallas_activas.geojson",
]
FAULTS_CACHE_FILE = "fallas_cache.json"


def _get_prop(props, keys, default=None):
    if not isinstance(props, dict):
        return default
    for k in keys:
        for pk in props.keys():
            if pk.lower() == k.lower():
                return props[pk]
    for k in keys:
        for pk in props.keys():
            if k.lower() in pk.lower():
                return props[pk]
    return default


def _coords_from_geometry(geom):
    if not isinstance(geom, dict):
        return []
    t = geom.get("type"); c = geom.get("coordinates")
    if not c:
        return []
    if t == "LineString":
        return [list(p)[:2] for p in c]
    if t == "MultiLineString":
        out = []
        for line in c:
            out.extend([list(p)[:2] for p in line])
        return out
    if t == "Polygon":
        return [list(p)[:2] for p in c[0]]
    if t == "MultiPolygon":
        return [list(p)[:2] for p in c[0][0]]
    if t == "Point":
        return [list(c)[:2]]
    return []


def _line_length_km(coords):
    total = 0.0
    for i in range(1, len(coords)):
        total += haversine_km(coords[i-1][1], coords[i-1][0], coords[i][1], coords[i][0])
    return round(total, 1)


def _mw_from_length(length_km):
    """Wells & Coppersmith (1994): Mw = 4.38 + 1.49*log10(SRL)."""
    if length_km is None or length_km <= 0:
        return None
    return round(min(9.5, 4.38 + 1.49 * math.log10(length_km)), 1)


def _parse_slip(v):
    if v is None:
        return None, None
    if isinstance(v, (int, float)):
        return float(v), float(v)
    nums = [float(x) for x in re.findall(r"\d+\.?\d*", str(v))][:2]
    if len(nums) == 2: return nums[0], nums[1]
    if len(nums) == 1: return nums[0], nums[0]
    return None, None


def normalize_falla(fid, props, geom, fuente):
    coords = _coords_from_geometry(geom)
    if len(coords) < 2:
        return None
    props = props or {}
    nombre = _get_prop(props, ["nombre","name","fault_name","faultname","name_es","fault"]) or f"Falla {fid}"
    tipo = str(_get_prop(props, ["tipo_falla","fault_type","type","style"], "desconocido"))
    actividad_raw = str(_get_prop(props, ["actividad","activity","age_class","last_event"], "activa")).lower()
    act = ("alta" if any(t in actividad_raw for t in ("alta","high","holoceno","histor","histór"))
           else "media" if any(t in actividad_raw for t in ("media","moderate","pleistoceno","tard"))
           else "baja")
    long_km = _line_length_km(coords)
    mw = _extract_number(_get_prop(props, ["mw_max","max_magnitude","mw_max_estimado","magnitude"]))
    if mw is None:
        mw = _mw_from_length(long_km)
    return {
        "id": fid,
        "nombre": nombre,
        "nombre_alternativo": str(_get_prop(props, ["nombre_alternativo","alias","alt_name"], "")),
        "pais": str(_get_prop(props, ["pais","country","country_name"], "—")),
        "continente": str(_get_prop(props, ["continente","continent"], "—")),
        "sistema_falla": str(_get_prop(props, ["sistema_falla","fault_system","system"], "—")),
        "tipo_falla": tipo,
        "actividad": act,
        "nivel_confianza": str(_get_prop(props, ["nivel_confianza","confidence","certainty"], "medio")),
        "lat_inicio": coords[0][1], "lon_inicio": coords[0][0],
        "lat_fin": coords[-1][1], "lon_fin": coords[-1][0],
        "longitud_km": long_km,
        "slip_rate_min": _parse_slip(_get_prop(props, ["slip_rate","slip_rate_mm_yr","sliprate"]))[0],
        "slip_rate_max": _parse_slip(_get_prop(props, ["slip_rate","slip_rate_mm_yr","sliprate"]))[1],
        "mw_max_estimado": mw,
        "profundidad_min": _extract_number(_get_prop(props, ["profundidad_min","depth_min"])),
        "profundidad_max": _extract_number(_get_prop(props, ["profundidad_max","depth_max"])),
        "recurrencia_min": _extract_number(_get_prop(props, ["recurrencia_min","recurrence_min"])),
        "recurrencia_max": _extract_number(_get_prop(props, ["recurrencia_max","recurrence_max"])),
        "coords": [[c[1], c[0]] for c in coords],   # [lat, lon]
        "fuente": fuente,
        "referencia": str(_get_prop(props, ["referencia","source","citation"], "")),
        "fecha_actualizacion": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def _embedded_fallas():
    out = []
    for i, (nombre, coords, tipo, act) in enumerate(FALLAS_GEOLOGICAS):
        # Aseguramos que el formato de coordenadas sea [lat, lon] puro para Leaflet
        lat_lons = [[c[0], c[1]] for c in coords]
        long_km = _line_length_km([[c[1], c[0]] for c in coords]) # inversión para haversine
        out.append({
            "id": f"EMB-{i}", 
            "nombre": nombre, 
            "nombre_alternativo": "",
            "pais": "Chile" if nombre == "San Ramón" else "—", 
            "continente": "América del Sur", 
            "sistema_falla": "Andino",
            "tipo_falla": tipo, 
            "actividad": act, 
            "nivel_confianza": "alto",
            "lat_inicio": lat_lons[0][0], "lon_inicio": lat_lons[0][1],
            "lat_fin": lat_lons[-1][0], "lon_fin": lat_lons[-1][1],
            "longitud_km": long_km,
            "slip_rate_min": 0.1, "slip_rate_max": 0.5,
            "mw_max_estimado": 7.5 if nombre == "San Ramón" else _mw_from_length(long_km),
            "profundidad_min": 2.0, "profundidad_max": 15.0,
            "recurrencia_min": 1000, "recurrencia_max": 5000,
            "coords": lat_lons,    # Formato directo [lat, lon] para Leaflet en api.py
            "fuente": "Catálogo embebido local",
            "referencia": "Estudios geológicos de falla activa", 
            "fecha_actualizacion": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        })
    return out


def fetch_all_faults(force=False):
    if not force and _os.path.exists(FAULTS_CACHE_FILE):
        try:
            age_h = (_time.time() - _os.path.getmtime(FAULTS_CACHE_FILE)) / 3600.0
            if age_h < 24:
                with open(FAULTS_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if cached:
                    return cached
        except Exception:
            pass

    fallas = []
    seen = set()

    def add(nf):
        if not nf: return
        key = (nf["nombre"] or "").lower()
        if key in seen: return
        seen.add(key)
        fallas.append(nf)

    # 1) GEM Global Active Faults
    gem = fetch_json(GEM_FAULTS_URL, timeout=240)
    if isinstance(gem, dict):
        for i, feat in enumerate(gem.get("features", [])):
            add(normalize_falla(f"GEM-{i}", feat.get("properties"), feat.get("geometry"), "GEM Global Active Faults"))

    # 2) USGS Quaternary Fault & Fold Database[cite: 1, 2]
    try:
        usgs = fetch_json(USGS_FAULTS_URL + "?where=1%3D1&outFields=*&outSR=4326&f=geojson&resultRecordCount=1500", timeout=120)
        if isinstance(usgs, dict):
            for i, feat in enumerate(usgs.get("features", [])):
                add(normalize_falla(f"USGS-{i}", feat.get("properties"), feat.get("geometry"), "USGS QFF"))
    except Exception as e:
        print("USGS faults error:", e)

    # 3) Chile (fallasactivas.cl)
    for url in CHILE_FAULTS_CANDIDATES:
        chl = fetch_json(url, timeout=60)
        if isinstance(chl, dict):
            for i, feat in enumerate(chl.get("features", [])):
                add(normalize_falla(f"CHILE-{i}", feat.get("properties"), feat.get("geometry"), "fallasactivas.cl"))

    # 4) Embebidas (respaldo offline)
    for nf in _embedded_fallas():
        add(nf)

    fallas.sort(key=lambda f: (f.get("mw_max_estimado") or 0), reverse=True)
    fallas = fallas[:800]

    try:
        with open(FAULTS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(fallas, f, ensure_ascii=False)
    except Exception as e:
        print("fallas cache error:", e)

    return fallas


# ============================================================
# Prueba directa (CORREGIDO: al FINAL del archivo)
# ============================================================

if __name__ == "__main__":
    result = run_pipeline()

    print("\nResumen:")
    print("Eventos:", len(result["events"]))
    print("Fenómenos:", len(result["phenomena"]))
    print("Riesgo por país:", len(result["risk"]))

    if not result["phenomena"].empty:
        result["phenomena"].to_csv(
            "client_table.csv",
            index=False,
            encoding="utf-8-sig",
        )
        print("Tabla cliente guardada en client_table.csv")

    if not result["risk"].empty:
        result["risk"].to_csv(
            "country_risk.csv",
            index=False,
            encoding="utf-8-sig",
        )
        print("Riesgo por país guardado en country_risk.csv")