
# -*- coding: utf-8 -*-
"""
SISMO-PREDICT API - Dashboard profesional en tiempo real.
Fuentes reales: USGS (sismos+fallas+geomag), NOAA SWPC (clima espacial),
NASA (NEO/Sentry/Horizons), CelesTrak/Space-Track (satélites), GEM (fallas).
"""

import os
import re
import json
import time
import threading
import requests
import numpy as np
import pandas as pd

from datetime import datetime, timedelta, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

import sismo_predict_b_auto as core

# ============================================================
# Configuración
# ============================================================

CACHE_FILE = "sismo_web_cache.json"
REFRESH_SECONDS = 5 * 60          # reconstrucción completa
RT_REFRESH_SECONDS = 60           # feed en tiempo real (antes que nadie)
DEFAULT_START = "1900-01-01"
MINMAG = 6.0

PLATES_URL = ("https://raw.githubusercontent.com/fraxen/tectonicplates/"
              "master/GeoJSON/PB2002_boundaries.json")

# Feeds en tiempo real de USGS (los más rápidos del mundo)
RT_FEEDS = {
    "hour": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
    "day25": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
}

MONTH_NUM = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
             "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}

EMBEDDED_VOLCANOES = [
    ("Kilauea",19.42,-155.29,"EEUU"),("Mauna Loa",19.48,-155.61,"EEUU"),
    ("Popocatépetl",19.02,-98.62,"México"),("Colima",19.51,-103.61,"México"),
    ("Fuego",14.47,-90.88,"Guatemala"),("Masaya",-11.98,-86.16,"Nicaragua"),
    ("Arenal",10.46,-84.70,"Costa Rica"),("Galeras",1.22,-77.36,"Colombia"),
    ("Nevado del Ruiz",4.89,-75.32,"Colombia"),("Cotopaxi",-0.68,-78.44,"Ecuador"),
    ("Tungurahua",-1.47,-78.44,"Ecuador"),("Sangay",-2.00,-78.34,"Ecuador"),
    ("Ubinas",-16.36,-70.90,"Perú"),("Misti",-16.29,-71.41,"Perú"),
    ("Villarrica",-39.42,-71.93,"Chile"),("Llaima",-38.69,-71.73,"Chile"),
    ("Osorno",-41.10,-72.49,"Chile"),("Calbuco",-41.33,-72.61,"Chile"),
    ("Chaitén",-42.83,-72.65,"Chile"),("Hudson",-45.90,-72.97,"Chile"),
    ("Lascar",-23.37,-67.73,"Chile"),("Fuji",35.36,138.73,"Japón"),
    ("Sakurajima",31.59,130.66,"Japón"),("Aso",32.88,131.10,"Japón"),
    ("Klyuchevskoy",56.06,160.64,"Rusia"),("Shiveluch",56.65,161.36,"Rusia"),
    ("Pinatubo",15.13,120.35,"Filipinas"),("Mayon",13.26,123.69,"Filipinas"),
    ("Taal",14.01,120.99,"Filipinas"),("Krakatau",-6.10,105.42,"Indonesia"),
    ("Merapi",-7.54,110.44,"Indonesia"),("Semeru",-8.11,112.92,"Indonesia"),
    ("Agung",-8.34,115.51,"Indonesia"),("Sinabung",3.17,98.39,"Indonesia"),
    ("Rinjani",-8.65,116.37,"Indonesia"),("Ruapehu",-39.28,175.57,"Nueva Zelanda"),
    ("Etna",37.75,15.00,"Italia"),("Stromboli",38.79,15.21,"Italia"),
    ("Vesubio",40.82,14.43,"Italia"),("Santorini",36.40,25.40,"Grecia"),
    ("Hekla",63.98,-19.70,"Islandia"),("Katla",63.63,-19.05,"Islandia"),
    ("Teide",28.27,-16.64,"España"),("Nyiragongo",-1.52,29.25,"RD Congo"),
    ("Nemrut",38.65,42.23,"Turquía"),("Erebus",-77.53,167.17,"Antártida"),
]

_lock = threading.Lock()
app = FastAPI(title="SISMO-PREDICT")


# ============================================================
# Utilidades
# ============================================================

def fetch_json(url, timeout=60):
    try:
        r = requests.get(url, headers={"User-Agent": "SismoPredict/1.0"}, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print("fetch_json error:", url, e)
    return None

_num = core._extract_number

def df_to_records(df):
    if df is None or df.empty:
        return []
    try:
        return json.loads(df.to_json(orient="records", date_format="iso"))
    except Exception:
        try:
            return json.loads(df.astype(str).to_json(orient="records"))
        except Exception:
            return []

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("load_cache error:", e)
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, default=str)
    except Exception as e:
        print("save_cache error:", e)


# ============================================================
# SISMOS EN TIEMPO REAL (antes que nadie)
# ============================================================

def fetch_realtime_quakes():
    """Descarga los sismos más recientes del mundo (última hora + último día)."""
    out = []
    for key, url in RT_FEEDS.items():
        data = fetch_json(url, timeout=30)
        if isinstance(data, dict):
            out.extend(core.parse_usgs_features(data.get("features", [])))
    return out


# ============================================================
# Placas, volcanes, magma, fallas
# ============================================================

def fetch_plates():
    data = fetch_json(PLATES_URL, timeout=120)
    if isinstance(data, dict) and "features" in data:
        return data
    return {"type": "FeatureCollection", "features": []}

def fetch_volcanoes():
    return [{"name": n, "lat": la, "lon": lo, "country": c} for n, la, lo, c in EMBEDDED_VOLCANOES]

def compute_magma_links(volcanoes, plates, step=8):
    coords = []
    for feature in plates.get("features", []):
        geom = feature.get("geometry", {})
        gtype = geom.get("type")
        if gtype == "LineString": lines = [geom.get("coordinates", [])]
        elif gtype == "MultiLineString": lines = geom.get("coordinates", [])
        else: continue
        for line in lines:
            if isinstance(line, list):
                coords.extend([c for c in line[::step]
                               if isinstance(c, (list, tuple)) and len(c) >= 2])
    if not coords or not volcanoes: return []
    try:
        blon = np.array([float(c[0]) for c in coords]); blat = np.array([float(c[1]) for c in coords])
    except Exception: return []
    links = []
    for v in volcanoes:
        x = np.cos(np.radians(v["lat"])) * (blon - v["lon"]); y = blat - v["lat"]
        idx = int(np.argmin(x*x + y*y))
        links.append({"volcano": v["name"], "from": [v["lon"], v["lat"]],
                      "to": [float(blon[idx]), float(blat[idx])]})
    return links

def procesar_fallas():
    try:
        return core.fetch_all_faults()
    except Exception as e:
        print("fetch_all_faults error:", e)
        return []


# ============================================================
# Campo magnético + clima espacial REAL
# ============================================================

def make_indicator(name, value, low, high, unit=""):
    if value is None:
        return {"name": name, "value": None, "status": "SIN DATOS", "color": "gray", "unit": unit}
    if value > high:
        return {"name": name, "value": round(value,2), "status": "ALTO", "color": "red", "unit": unit}
    if value < low:
        return {"name": name, "value": round(value,2), "status": "BAJO", "color": "blue", "unit": unit}
    return {"name": name, "value": round(value,2), "status": "NORMAL", "color": "green", "unit": unit}

def fetch_magnetic():
    out = {"indicators": [], "kp_series": [],
           "note": "Fuentes reales: NOAA SWPC y USGS geomagnetismo."}
    kp = fetch_json("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json")
    if isinstance(kp, list) and kp:
        series = [{"t": e.get("time_tag"), "kp": _num(e.get("kp"))}
                  for e in kp[-48:] if _num(e.get("kp")) is not None]
        out["kp_series"] = series
        if series:
            out["indicators"].append(make_indicator("Índice Kp", series[-1]["kp"], 0, 4))
    goes = fetch_json("https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json")
    if isinstance(goes, list) and goes:
        last = goes[-1]
        out["indicators"].append(make_indicator("IMF Bz", _num(last.get("Bz")), -5, 5, "nT"))
        out["indicators"].append(make_indicator("Campo Bt", _num(last.get("Bt")), 2, 20, "nT"))
    return out

def fetch_spaceweather_extra():
    """Datos reales adicionales de NOAA SWPC."""
    out = {"xray_series": [], "radio_flux": None, "sunspot": None, "indicators": []}
    xr = fetch_json("https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json")
    if isinstance(xr, list):
        out["xray_series"] = [{"t": e.get("time_tag"), "v": _num(e.get("flux"))} for e in xr[-72:]]
        if out["xray_series"]:
            out["indicators"].append(make_indicator("X-ray GOES", out["xray_series"][-1]["v"], 1e-8, 1e-5, "W/m²"))
    srf = fetch_json("https://services.swpc.noaa.gov/json/solar-radio-flux.json")
    if isinstance(srf, list) and srf:
        out["radio_flux"] = _num(srf[-1].get("flux"))
        out["indicators"].append(make_indicator("Radio-flux 10.7", out["radio_flux"], 70, 200, "sfu"))
    ss = fetch_json("https://services.swpc.noaa.gov/json/sunspot_report.json")
    if isinstance(ss, dict):
        out["sunspot"] = _num(ss.get("ssn"))
        out["indicators"].append(make_indicator("Manchas solares", out["sunspot"], 0, 150, ""))
    return out


# ============================================================
# Construcción de caché
# ============================================================

def _sort_phenomena_desc(records):
    def key(r):
        y = r.get("Año") or 0
        dm = r.get("Día y Mes") or ""
        m = re.match(r"(\d+) de (\w+)", dm)
        day = int(m.group(1)) if m else 0
        mon = MONTH_NUM.get((m.group(2) if m else "").lower(), 0)
        return (y, mon, day)
    return sorted(records, key=key, reverse=True)

def build_cache(force=False):
    with _lock:
        cache = load_cache()
        now = datetime.now(timezone.utc)

        if not force:
            last_update = cache.get("metadata", {}).get("last_update_utc")
            if last_update:
                try:
                    if (now - datetime.fromisoformat(last_update)).total_seconds() < REFRESH_SECONDS:
                        return cache
                except Exception:
                    pass

        last_event_time = cache.get("metadata", {}).get("last_event_time")
        if last_event_time:
            try:
                start = (pd.to_datetime(last_event_time, utc=True) - timedelta(days=1)).strftime("%Y-%m-%d")
            except Exception: start = DEFAULT_START
        else:
            start = (now - timedelta(days=365*10)).strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")

        try:
            print(f"Descargando USGS {start} -> {end}")
            new_events = core.parse_usgs_features(core.fetch_usgs_range(start, end, MINMAG, chunk_days=365))
        except Exception as e:
            print("Error USGS:", e); new_events = pd.DataFrame()

        rt = fetch_realtime_quakes()   # <- sismos de AHORA (antes que nadie)

        existing = pd.DataFrame(cache.get("events", []))
        if not existing.empty and "time_utc" in existing.columns:
            try: existing["time_utc"] = pd.to_datetime(existing["time_utc"], utc=True)
            except Exception: pass

        try: seed = core.load_manual_seed()
        except Exception: seed = pd.DataFrame()

        frames = [df for df in [existing, new_events, pd.DataFrame(rt), seed]
                  if df is not None and not df.empty]
        events = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

        phenomena = pd.DataFrame(); risk = pd.DataFrame()
        if not events.empty:
            for col in ["latitude","longitude","mag","place"]:
                if col not in events.columns: events[col] = np.nan
            if "source" not in events.columns: events["source"] = "usgs"
            try: events = core.deduplicate_events(events)
            except Exception as e: print("dedup:", e)
            try: events = core.add_country(events)
            except Exception: events["country"] = "Desconocido"
            try: events = core.add_local_time(events)
            except Exception:
                events["time_local"] = [pd.Timestamp(t).replace(tzinfo=None) for t in events["time_utc"]]
            try: events["year"] = events["time_utc"].dt.year
            except Exception: pass
            try: events["day_month"] = events["time_local"].apply(core.format_day_month)
            except Exception: pass
            try: events = core.detect_doublets(events, min_mag=MINMAG)
            except Exception: pass
            try: events = core.add_event_impact(events)
            except Exception: pass
            try: phenomena = core.build_phenomenon_table(events)
            except Exception as e: print("phenomena:", e)
            try: risk = core.country_risk_table(phenomena=phenomena, events=events, min_mag=MINMAG)
            except Exception as e: print("risk:", e)

        plates = cache.get("plates") or fetch_plates()
        volcanoes = cache.get("volcanoes") or fetch_volcanoes()
        magma_links = cache.get("magma_links") or compute_magma_links(volcanoes, plates)
        fallas = cache.get("fallas") or procesar_fallas()

        cache = {
            "metadata": {
                "last_update_utc": now.isoformat(),
                "rt_update_utc": now.isoformat(),
                "last_event_time": str(events["time_utc"].max()) if not events.empty else None,
                "total_events": len(events),
            },
            "events": df_to_records(events),
            "rt_events": df_to_records(pd.DataFrame(rt))[:500],
            "phenomena": _sort_phenomena_desc(df_to_records(phenomena)),
            "risk": df_to_records(risk),
            "plates": plates, "volcanoes": volcanoes,
            "magma_links": magma_links, "fallas": fallas,
            "magnetic": fetch_magnetic(),
            "space_extra": fetch_spaceweather_extra(),
            "plate_motion": [{"plate":p[0],"lat":p[1],"lon":p[2],"azimuth":p[3],"speed":p[4]}
                             for p in getattr(core, "PLATE_MOTION", [])],
            "forecasts": core.generate_forecasts(events, phenomena, risk) if not events.empty else [],
            "alerts": core.generate_alerts(events, []) if not events.empty else [],
        }
        save_cache(cache)
        return cache


def rt_updater():
    """Hilo que actualiza sismos en tiempo real cada 60 s."""
    while True:
        time.sleep(RT_REFRESH_SECONDS)
        try:
            rt = fetch_realtime_quakes()
            if not rt: continue
            with _lock:
                cache = load_cache()
                old = cache.get("rt_events", [])
                ids = set(e.get("id") for e in rt)
                merged = df_to_records(pd.DataFrame(rt)) + [e for e in old if e.get("id") not in ids]
                cache["rt_events"] = merged[:500]
                cache.setdefault("metadata", {})["rt_update_utc"] = datetime.now(timezone.utc).isoformat()
                save_cache(cache)
        except Exception as e:
            print("rt_updater error:", e)

def background_updater():
    while True:
        time.sleep(REFRESH_SECONDS)
        try: build_cache(force=True)
        except Exception as e: print("background_updater error:", e)


@app.on_event("startup")
def startup():
    try: build_cache(force=False)
    except Exception as e: print("startup error:", e)
    threading.Thread(target=background_updater, daemon=True).start()
    threading.Thread(target=rt_updater, daemon=True).start()


@app.get("/", response_class=HTMLResponse)
def dashboard(): return DASHBOARD_HTML

@app.get("/api/data")
def api_data():
    try: return JSONResponse(load_cache())
    except Exception as e: return JSONResponse({"error": str(e)})

@app.get("/api/sky")
def api_sky():
    return JSONResponse({
        "iss": core.fetch_iss(),
        "satellites": core.fetch_satellites(),
        "launches": core.fetch_launches(),
        "reentries": core.get_reentries(),
        "asteroids": core.fetch_asteroids(),
    })

@app.get("/api/space")
def api_space():
    return JSONResponse({
        "weather": core.fetch_spaceweather(),
        "extra": fetch_spaceweather_extra(),
        "sentry": core.fetch_sentry(),
        "orbits": core.fetch_orbits(),
        "ozone": core.fetch_ozone(),
    })

@app.get("/api/refresh")
def refresh():
    try:
        build_cache(force=True); return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# ============================================================
# Dashboard HTML (head + CSS + body)
# ============================================================

DASHBOARD_HTML = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SISMO-PREDICT | Panel en tiempo real</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0b1220;--card:#111a2e;--line:#23304d;--text:#e6ecf7;--muted:#8fa1c0;
--red:#ff4d4d;--blue:#3aa0ff;--green:#2ecc71;--orange:#ff9f43;--violet:#a29bfe}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:Segoe UI,Roboto,Arial}
header{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;
border-bottom:1px solid var(--line);background:#0d1526;flex-wrap:wrap;gap:10px}
header h1{font-size:20px}header h1 span{color:var(--orange)}
.dot{width:10px;height:10px;border-radius:50%;background:var(--green);display:inline-block;
margin-right:6px;animation:pulse 1.5s infinite}
@keyframes pulse{0%{opacity:1}50%{opacity:.3}100%{opacity:1}}
button{background:var(--violet);border:none;color:#08101f;padding:7px 12px;border-radius:8px;
cursor:pointer;font-weight:600}
.banner{padding:10px 20px;background:rgba(255,77,77,.15);color:var(--red);
border-bottom:1px solid var(--line);font-weight:700;display:none}
.banner.on{display:block}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:14px;padding:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
#map{height:70vh;min-height:520px;border-radius:10px}
.side{display:flex;flex-direction:column;gap:14px}
h3{font-size:13px;color:var(--muted);margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px}
.badge{padding:3px 8px;border-radius:6px;font-size:11px;font-weight:700;white-space:nowrap}
.red{background:rgba(255,77,77,.15);color:var(--red)}
.blue{background:rgba(58,160,255,.15);color:var(--blue)}
.green{background:rgba(46,204,113,.15);color:var(--green)}
.gray{background:rgba(150,150,150,.15);color:#aaa}
.row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;
border-bottom:1px dashed var(--line);gap:8px}
.row:last-child{border-bottom:none}
.row small{color:var(--muted);display:block;margin-top:2px}
table{width:100%;border-collapse:collapse;font-size:12px}
th,td{padding:7px 8px;text-align:left;border-bottom:1px solid var(--line)}
th{color:var(--muted);position:sticky;top:0;background:var(--card)}
.controls{margin-top:10px;display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);
padding:8px;background:#0d1526;border-radius:8px;border:1px solid var(--line)}
.controls label{display:inline-flex;align-items:center;gap:4px;cursor:pointer}
.controls input{accent-color:var(--violet)}
.note{font-size:11px;color:var(--muted);margin-top:8px;line-height:1.4}
.duo{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.trio{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
canvas.mini{width:100%;height:260px;background:#0d1526;border:1px solid var(--line);border-radius:10px}
#minimap{height:260px;border-radius:10px;border:1px solid var(--line)}
.listbox{max-height:140px;overflow:auto;margin-top:8px;font-size:11px}
.pred-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.pred{background:#0d1526;border:1px solid var(--line);border-left:3px solid var(--violet);
border-radius:8px;padding:12px}
.pred .f{font-size:12px;color:var(--muted);display:block;margin-top:3px}
.table-wrap{max-height:380px;overflow:auto;border-radius:8px;border:1px solid var(--line)}
.falla-nombre{color:#ff8080;font-size:10px;font-weight:bold;text-shadow:1px 1px 2px #000;
white-space:nowrap;text-align:center;pointer-events:none}
.legend{background:#0d1526;border:1px solid var(--line);border-radius:8px;padding:8px 10px;
color:var(--text);font-size:11px;line-height:1.7}
.lg-line{width:18px;height:3px;display:inline-block;margin-right:6px;vertical-align:middle}
.lg-hatch{width:18px;height:12px;display:inline-block;margin-right:6px;vertical-align:middle;border:1px solid #666}
@media(max-width:1100px){.layout{grid-template-columns:1fr}.duo,.trio{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <h1>🌍 SISMO<span>-PREDICT</span> | Tiempo real</h1>
  <div><span class="dot"></span> En vivo · <span id="lastupdate">-</span>
  <button onclick="manualRefresh()">↻ Actualizar</button></div>
</header>
<div id="banner" class="banner"></div>

<div class="layout">
  <section class="card">
    <h3>🗺️ Mapa tectónico global</h3>
    <div id="map"></div>
    <div class="controls">
      <label><input type="checkbox" id="ly_plates" checked> Placas</label>
      <label><input type="checkbox" id="ly_fallas" checked> Fallas</label>
      <label><input type="checkbox" id="ly_quakes" checked> Sismos</label>
      <label><input type="checkbox" id="ly_volc" checked> Volcanes</label>
      <label><input type="checkbox" id="ly_magma" checked> Magma</label>
      <label><input type="checkbox" id="ly_sats" checked> Satélites</label>
      <span>|</span>
      <label><input type="radio" name="qrange" value="month"> Mes</label>
      <label><input type="radio" name="qrange" value="year"> Año</label>
      <label><input type="radio" name="qrange" value="all" checked> Todos</label>
    </div>
    <div class="note">Círculos con textura 45° = zona de desastre estimada. Rojo = falla activa.</div>
  </section>

  <aside class="side">
    <div class="card"><h3><span class="dot"></span>ISS · Telemetría</h3><div id="iss_live"></div></div>
    <div class="card"><h3>☀️ Clima espacial (real)</h3>
      <canvas id="sw_anim" class="mini" style="height:140px"></canvas>
      <canvas id="ch_xray" class="mini" style="height:90px;margin-top:8px"></canvas>
      <div id="sw_gauges"></div></div>
    <div class="card"><h3>📡 Sensores geofísicos</h3><div id="sensors"></div></div>
    <div class="card"><h3>🧲 Campo magnético</h3><div id="magnetic"></div></div>
    <div class="card"><h3>⚠️ Alertas</h3><div id="alerts"></div></div>
    <div class="card"><h3>📈 Prob. 10 años</h3><div id="predict"></div></div>
  </aside>

  <div class="duo">
    <div class="card"><h3>🛰️ Órbitas en vivo</h3><div id="minimap"></div>
      <div class="listbox" id="sat_list"></div></div>
    <div class="card"><h3>🗑️ Radar de debris</h3><canvas id="debris_radar" class="mini"></canvas>
      <div class="listbox" id="debris_list"></div></div>
  </div>

  <div class="trio">
    <div class="card"><h3>🪐 Sistema solar (trayectorias)</h3>
      <canvas id="solar_map" class="mini"></canvas><div class="listbox" id="solar_list"></div></div>
    <div class="card"><h3>☄️ Radar NEO</h3><canvas id="neo_radar" class="mini"></canvas>
      <div class="listbox" id="neo_list"></div></div>
    <div class="card"><h3>🕳️ Ozono + anomalías</h3><div id="ozone_card"></div>
      <div id="anomaly_card" style="margin-top:8px"></div></div>
  </div>

  <section class="card" style="grid-column:1/-1">
    <h3>🔮 Predicciones futuras</h3><div id="forecast" class="pred-grid"></div>
  </section>

  <section class="card" style="grid-column:1/-1">
    <h3>📋 Tabla de fenómenos (más recientes primero)</h3>
    <div class="table-wrap"><table id="pheno"></table></div>
  </section>

  <div class="trio">
    <div class="card"><h3>📊 Magnitudes</h3><canvas id="ch_mag" class="mini" style="height:180px"></canvas></div>
    <div class="card"><h3>📅 Eventos/año</h3><canvas id="ch_year" class="mini" style="height:180px"></canvas></div>
    <div class="card"><h3>📶 Kp (48h)</h3><canvas id="ch_kp" class="mini" style="height:180px"></canvas></div>
  </div>
</div>
"""

# ============================================================
# Dashboard HTML (PARTE 2: JavaScript completo)
# ============================================================

DASHBOARD_HTML += """
<script>
console.log("=== SISMO-PREDICT Dashboard v2 (tiempo real) ===");

/* ==========================================================
   1) VARIABLES GLOBALES
   ========================================================== */
var DATA = null;
var SKY = { iss: null, satellites: [], launches: [], reentries: [], asteroids: [] };
var SPACE = { weather: {}, extra: {}, sentry: [], orbits: [], ozone: null };
var CH = {};
var Q_RANGE = "all";

var SOLAR_VIEW = { scale: 1, ox: 0, oy: 0 };
var RADAR_VIEW = { scale: 1, ox: 0, oy: 0 };
var DEBRIS_VIEW = { scale: 1, ox: 0, oy: 0 };
var SOLAR_PTS = [], RADAR_PTS = [], DEBRIS_PTS = [];

var swT = 0, debA = 0, neoA = 0;

/* ==========================================================
   2) MAPA PRINCIPAL (grande) + teselas
   ========================================================== */
var map = L.map("map", { worldCopyJump: true, zoomSnap: 0.5 }).setView([10, -40], 2);
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution: "©OpenStreetMap", maxZoom: 18
}).addTo(map);

/* ----------------------------------------------------------
   Renderer SVG con PATRONES DE TEXTURA 45° (cortes geológicos)
   ---------------------------------------------------------- */
var hatchRenderer = L.svg().addTo(map);
(function () {
  try {
    var svg = hatchRenderer._container;
    var NS = "http://www.w3.org/2000/svg";
    var defs = document.createElementNS(NS, "defs");
    [["hatch-red", "#ff4d4d"], ["hatch-orange", "#ff9f43"], ["hatch-yellow", "#ffd166"]].forEach(function (p) {
      var pat = document.createElementNS(NS, "pattern");
      pat.setAttribute("id", p[0]);
      pat.setAttribute("patternUnits", "userSpaceOnUse");
      pat.setAttribute("width", "8");
      pat.setAttribute("height", "8");
      pat.setAttribute("patternTransform", "rotate(45)");
      var line = document.createElementNS(NS, "line");
      line.setAttribute("x1", "0"); line.setAttribute("y1", "0");
      line.setAttribute("x2", "0"); line.setAttribute("y2", "8");
      line.setAttribute("stroke", p[1]);
      line.setAttribute("stroke-width", "2");
      pat.appendChild(line);
      defs.appendChild(pat);
    });
    svg.appendChild(defs);
  } catch (err) { console.error("hatch defs:", err); }
})();

/* ----------------------------------------------------------
   LEYENDA (fallas + zonas de desastre)
   ---------------------------------------------------------- */
var legend = L.control({ position: "bottomright" });
legend.onAdd = function () {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML =
    "<b>Leyenda</b><br>" +
    '<span class="lg-line" style="background:#ff0000"></span> Falla act. alta<br>' +
    '<span class="lg-line" style="background:#ff6b35"></span> Falla act. media<br>' +
    '<span class="lg-line" style="background:#ffa500"></span> Falla act. baja<br>' +
    '<span class="lg-hatch" style="background:repeating-linear-gradient(45deg,transparent 0 3px,#ff4d4d 3px 5px)"></span> Desastre M≥8<br>' +
    '<span class="lg-hatch" style="background:repeating-linear-gradient(45deg,transparent 0 3px,#ff9f43 3px 5px)"></span> Desastre M7–8<br>' +
    '<span class="lg-hatch" style="background:repeating-linear-gradient(45deg,transparent 0 3px,#ffd166 3px 5px)"></span> Desastre M6–7<br>' +
    '<span class="lg-line" style="background:#7aa2ff"></span> Límite de placa';
  return div;
};
legend.addTo(map);

/* ----------------------------------------------------------
   Grupos de capas
   ---------------------------------------------------------- */
var G = {
  plates: L.layerGroup(), fallas: L.layerGroup(), falla_labels: L.layerGroup(),
  zonas: L.layerGroup(), quakes: L.layerGroup(), volc: L.layerGroup(),
  magma: L.layerGroup(), motion: L.layerGroup(), sats: L.layerGroup()
};
Object.keys(G).forEach(function (k) { G[k].addTo(map); });

/* ----------------------------------------------------------
   MINIMAPA (órbitas en vivo)
   ---------------------------------------------------------- */
var minimap = L.map("minimap", { zoomControl: true, attributionControl: false }).setView([10, -40], 1);
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png").addTo(minimap);
var MINI_SATS = L.layerGroup().addTo(minimap);
var issTrail = [];
var issTrailLine = null;

function fixMapSize() {
  setTimeout(function () {
    try { map.invalidateSize(); minimap.invalidateSize(); } catch (e) {}
  }, 300);
}
window.addEventListener("resize", fixMapSize);

/* ==========================================================
   3) UTILIDADES
   ========================================================== */
function calcularRadioAfectacion(mag, prof) {
  mag = mag || 0; prof = prof || 10;
  var r;
  if (mag < 2) r = 5;
  else if (mag < 4) r = 10 + (mag - 2) * 15;
  else if (mag < 6) r = 40 + (mag - 4) * 50;
  else if (mag < 7) r = 140 + (mag - 6) * 150;
  else if (mag < 8) r = 290 + (mag - 7) * 300;
  else r = 590 + (mag - 8) * 500;
  if (prof > 100) r *= 1.5;
  else if (prof > 50) r *= 1.2;
  return Math.round(r);
}

function colorQuake(t) {
  var d = (Date.now() - new Date(t)) / 86400000;
  return d < 7 ? "#ff4d4d" : d < 30 ? "#ff9f43" : d < 365 ? "#ffd166" : "#8fa1c0";
}

function inRange(t) {
  if (Q_RANGE === "all") return true;
  var d = (Date.now() - new Date(t)) / 86400000;
  return Q_RANGE === "month" ? d <= 30 : d <= 365;
}

function haversineKm(a1, o1, a2, o2) {
  var R = 6371, dA = (a2 - a1) * Math.PI / 180, dO = (o2 - o1) * Math.PI / 180;
  var s = Math.sin(dA / 2) * Math.sin(dA / 2) +
    Math.cos(a1 * Math.PI / 180) * Math.cos(a2 * Math.PI / 180) * Math.sin(dO / 2) * Math.sin(dO / 2);
  return R * 2 * Math.atan2(Math.sqrt(s), Math.sqrt(1 - s));
}

function fallaPopup(f) {
  return "<b>🔴 " + (f.nombre || "") + "</b><br>" +
    "<small>Alt: " + (f.nombre_alternativo || "-") + " · País: " + (f.pais || "-") + "</small><br>" +
    "Sistema: " + (f.sistema_falla || "-") + " · Tipo: " + (f.tipo_falla || "-") + "<br>" +
    "Actividad: " + (f.actividad || "-") + " · Confianza: " + (f.nivel_confianza || "-") + "<br>" +
    "Longitud: " + (f.longitud_km || "-") + " km<br>" +
    "Slip: " + (f.slip_rate_min || "-") + "–" + (f.slip_rate_max || "-") + " mm/a<br>" +
    "<b>Mw máx: " + (f.mw_max_estimado || "-") + "</b><br>" +
    "Prof: " + (f.profundidad_min || "-") + "–" + (f.profundidad_max || "-") + " km<br>" +
    "Recurrencia: " + (f.recurrencia_min || "-") + "–" + (f.recurrencia_max || "-") + " años<br>" +
    "<small>Fuente: " + (f.fuente || "-") + "</small>";
}

/* ----------------------------------------------------------
   Canvas con zoom + arrastre + identificación al cursor
   ---------------------------------------------------------- */
function makeZoomable(id, view, getPts) {
  var cv = document.getElementById(id);
  if (!cv) return;
  cv.addEventListener("wheel", function (e) {
    e.preventDefault();
    view.scale = Math.min(12, Math.max(0.5, view.scale * (e.deltaY < 0 ? 1.2 : 1 / 1.2)));
  }, { passive: false });
  var drag = null;
  cv.addEventListener("mousedown", function (e) { drag = { x: e.clientX, y: e.clientY, ox: view.ox, oy: view.oy }; });
  window.addEventListener("mousemove", function (e) { if (drag) { view.ox = drag.ox + (e.clientX - drag.x); view.oy = drag.oy + (e.clientY - drag.y); } });
  window.addEventListener("mouseup", function () { drag = null; });
  cv.addEventListener("mousemove", function (e) {
    var pts = getPts();
    var best = null, bd = 169;
    pts.forEach(function (p) {
      var dx = p.x - e.offsetX, dy = p.y - e.offsetY, d = dx * dx + dy * dy;
      if (d < bd) { bd = d; best = p; }
    });
    var tip = document.getElementById("space_tip");
    if (!tip) {
      tip = document.createElement("div"); tip.id = "space_tip";
      tip.style.cssText = "position:fixed;background:#0d1526;border:1px solid var(--line);border-radius:6px;padding:6px;font-size:11px;pointer-events:none;z-index:999;display:none";
      document.body.appendChild(tip);
    }
    if (best) {
      tip.style.display = "block";
      tip.style.left = (e.clientX + 12) + "px";
      tip.style.top = (e.clientY + 12) + "px";
      tip.innerHTML = best.info;
    } else tip.style.display = "none";
  });
}
makeZoomable("solar_map", SOLAR_VIEW, function () { return SOLAR_PTS; });
makeZoomable("neo_radar", RADAR_VIEW, function () { return RADAR_PTS; });
makeZoomable("debris_radar", DEBRIS_VIEW, function () { return DEBRIS_PTS; });

/* ==========================================================
   4) CARGA DE DATOS (3 flujos: cache, cielo, espacio)
   ========================================================== */
function load() {
  return fetch("/api/data").then(function (r) { return r.json(); }).then(function (d) {
    DATA = d;
    render(d);
  }).catch(function (e) { console.error("load:", e); });
}

function loadSky() {
  return fetch("/api/sky").then(function (r) { return r.json(); }).then(function (s) {
    SKY = s || {};
    renderSky();
  }).catch(function (e) { console.error("sky:", e); });
}

function loadSpace() {
  return fetch("/api/space").then(function (r) { return r.json(); }).then(function (s) {
    SPACE = s || {};
    renderSpace();
  }).catch(function (e) { console.error("space:", e); });
}

function manualRefresh() {
  fetch("/api/refresh").then(function () { return load(); })
    .catch(function (e) { console.error("refresh:", e); });
}

/* ==========================================================
   5) RENDER PRINCIPAL
   ========================================================== */
function render(data) {
  if (!data) return;

  try {
    document.getElementById("lastupdate").textContent =
      ((data.metadata && (data.metadata.rt_update_utc || data.metadata.last_update_utc)) || "")
        .slice(0, 19).replace("T", " ");
  } catch (err) { console.error("metadata:", err); }

  try {
    var bn = document.getElementById("banner");
    var hi = (data.alerts || []).filter(function (a) { return a.nivel === "ALTO"; });
    if (hi.length) { bn.classList.add("on"); bn.textContent = "⚠ ALERTA: " + hi[0].mensaje; }
    else { bn.classList.remove("on"); bn.textContent = ""; }
  } catch (err) { console.error("banner:", err); }

  try {
    G.plates.clearLayers(); G.fallas.clearLayers(); G.falla_labels.clearLayers();
    G.zonas.clearLayers(); G.quakes.clearLayers(); G.volc.clearLayers();
    G.magma.clearLayers(); G.motion.clearLayers();
  } catch (err) { console.error("clear:", err); }

  renderPlates(data);
  renderFallas(data);
  renderQuakes(data);
  renderVolcMagmaMotion(data);
  renderSide(data);
  renderTable(data);
  renderForecast(data);
  renderCharts(data);
  fixMapSize();
}

/* ----------------------------------------------------------
   5a) Placas + nombres
   ---------------------------------------------------------- */
function renderPlates(data) {
  try {
    if (data.plates && data.plates.features) {
      L.geoJSON(data.plates, {
        style: { color: "#7aa2ff", weight: 1, opacity: 0.7 },
        onEachFeature: function (f, layer) {
          if (f.properties && f.properties.name)
            layer.bindTooltip(f.properties.name, { sticky: true });
        }
      }).addTo(G.plates);
    }
  } catch (err) { console.error("placas:", err); }
}

/* ----------------------------------------------------------
   5b) FALLAS: línea roja + nombre + zona de desastre 45°
   ---------------------------------------------------------- */
function renderFallas(data) {
  try {
    (data.fallas || []).forEach(function (f) {
      var coords = (f.coords || []).map(function (c) { return [c[0], c[1]]; });
      if (coords.length < 2) return;

      var col = f.actividad === "alta" ? "#ff0000" : f.actividad === "media" ? "#ff6b35" : "#ffa500";

      var line = L.polyline(coords, { color: col, weight: 2, opacity: 0.85, renderer: hatchRenderer });
      line.bindTooltip("<b>" + (f.nombre || "") + "</b><br>Tipo: " + (f.tipo_falla || "-") +
        "<br>Mw máx: " + (f.mw_max_estimado || "-"), { sticky: true });
      line.on("click", function () { L.popup({ maxWidth: 320 }).setContent(fallaPopup(f)).openOn(map); });
      line.addTo(G.fallas);

      var mid = coords[Math.floor(coords.length / 2)];
      L.marker(mid, {
        icon: L.divIcon({
          className: "falla-label",
          html: '<div class="falla-nombre">' + (f.nombre || "") + '</div>',
          iconSize: [130, 14], iconAnchor: [65, 7]
        })
      }).addTo(G.falla_labels);

      var mw = f.mw_max_estimado || 6.5;
      if (mw >= 6.5) {
        var radio = calcularRadioAfectacion(mw, f.profundidad_min || 10);
        var pc = mw >= 8 ? "hatch-red" : mw >= 7 ? "hatch-orange" : "hatch-yellow";
        L.circle(mid, {
          radius: radio * 1000, renderer: hatchRenderer,
          fillColor: "url(#" + pc + ")", fillOpacity: 0.35,
          color: col, weight: 1, dashArray: "4 4", opacity: 0.7
        }).bindTooltip("Zona de desastre M" + mw + ": ~" + radio + " km").addTo(G.zonas);
      }
    });

    function toggleLabels() {
      if (map.getZoom() >= 5) { if (!map.hasLayer(G.falla_labels)) G.falla_labels.addTo(map); }
      else { map.removeLayer(G.falla_labels); }
    }
    map.off("zoomend", toggleLabels);
    map.on("zoomend", toggleLabels);
    toggleLabels();
  } catch (err) { console.error("fallas:", err); }
}

/* ----------------------------------------------------------
   5c) SISMOS (históricos + EN VIVO) + zonas de desastre
   ---------------------------------------------------------- */
function renderQuakes(data) {
  try {
    var all = (data.events || []).concat(data.rt_events || []);
    var seen = {};
    all.forEach(function (e) {
      if (!e || e.mag == null || e.latitude == null || e.longitude == null) return;
      if (seen[e.id]) return; seen[e.id] = 1;
      var la = +e.latitude, lo = +e.longitude;
      if (isNaN(la) || isNaN(lo)) return;
      if (!inRange(e.time_utc)) return;

      L.circleMarker([la, lo], {
        radius: Math.max(2, e.mag * 1.6),
        color: colorQuake(e.time_utc), fillColor: colorQuake(e.time_utc),
        fillOpacity: 0.5, weight: 1
      }).bindTooltip("M" + e.mag + "<br>" + (e.place || "") + "<br>" + (e.time_utc || "").slice(0, 10))
        .addTo(G.quakes);

      if (e.mag >= 6) {
        var r = calcularRadioAfectacion(e.mag, e.depth_km || 10);
        var pc = e.mag >= 8 ? "hatch-red" : e.mag >= 7 ? "hatch-orange" : "hatch-yellow";
        L.circle([la, lo], {
          radius: r * 1000, renderer: hatchRenderer,
          fillColor: "url(#" + pc + ")", fillOpacity: 0.3,
          color: "#ff4d4d", weight: 1, dashArray: "4 4", opacity: 0.6
        }).bindTooltip("Zona de desastre M" + e.mag + ": ~" + r + " km").addTo(G.quakes);
      }
    });
  } catch (err) { console.error("sismos:", err); }
}

/* ----------------------------------------------------------
   5d) Volcanes, magma, movimiento de placas
   ---------------------------------------------------------- */
function renderVolcMagmaMotion(data) {
  try {
    (data.volcanoes || []).forEach(function (v) {
      L.marker([+v.lat, +v.lon], {
        icon: L.divIcon({ className: "", html: '<div style="color:#ff9f43;font-size:14px">▲</div>' })
      }).bindTooltip("🌋 " + v.name + " (" + v.country + ")").addTo(G.volc);
    });
  } catch (err) { console.error("volcanes:", err); }

  try {
    (data.magma_links || []).forEach(function (l) {
      L.polyline([[+l.from[1], +l.from[0]], [+l.to[1], +l.to[0]]],
        { color: "#ff5c5c", dashArray: "4 6", weight: 1, opacity: 0.6 })
        .bindTooltip("Magma → " + l.volcano).addTo(G.magma);
    });
  } catch (err) { console.error("magma:", err); }

  try {
    (data.plate_motion || []).forEach(function (p) {
      var az = p.azimuth * Math.PI / 180;
      var cosLat = Math.max(0.2, Math.cos(p.lat * Math.PI / 180));
      var tail = [p.lat - Math.cos(az) * 8, p.lon - Math.sin(az) * 8 / cosLat];
      L.polyline([tail, [p.lat, p.lon]], { color: "#2ecc71", weight: 2, opacity: 0.85, dashArray: "2 4" }).addTo(G.motion);
      L.marker([p.lat, p.lon], {
        icon: L.divIcon({
          className: "", iconSize: [16, 16],
          html: '<div style="color:#2ecc71;transform:rotate(' + (p.azimuth - 90) + 'deg);font-size:16px">➤</div>'
        })
      }).bindTooltip(p.plate + ": " + p.speed + " cm/año").addTo(G.motion);
    });
  } catch (err) { console.error("mov placas:", err); }
}

/* ==========================================================
   6) PANEL LATERAL (sensores reales)
   ========================================================== */
function renderSide(data) {
  try {
    var mag = data.magnetic || {};
    var m = document.getElementById("magnetic");
    m.innerHTML = "";
    (mag.indicators || []).forEach(function (i) {
      m.innerHTML += '<div class="row"><span>' + i.name + '</span><span class="badge ' + i.color + '">' +
        (i.value != null ? i.value : "-") + " " + (i.unit || "") + " · " + i.status + "</span></div>";
    });
    if (!(mag.indicators || []).length) m.innerHTML = '<div class="note">Sin datos magnéticos.</div>';
  } catch (err) { console.error("magnético:", err); }

  try {
    var extra = data.space_extra || {};
    var s = document.getElementById("sensors");
    s.innerHTML = "";
    (extra.indicators || []).forEach(function (i) {
      s.innerHTML += '<div class="row"><span>' + i.name + '</span><span class="badge ' + i.color + '">' +
        (i.value != null ? i.value : "-") + " " + (i.unit || "") + " · " + i.status + "</span></div>";
    });
    var now = Date.now(), week = 0, total = 0;
    (data.events || []).forEach(function (e) {
      total++;
      if ((now - new Date(e.time_utc)) / 86400000 <= 7) week++;
    });
    var base = total / 104;
    var ratio = base > 0 ? week / base : 0;
    var st = ratio > 1.5 ? ["ALTO", "red"] : ratio < 0.5 ? ["BAJO", "blue"] : ["NORMAL", "green"];
    s.innerHTML += '<div class="row"><span>Actividad sísmica (7d)</span><span class="badge ' + st[1] + '">' +
      ratio.toFixed(2) + "x · " + st[0] + "</span></div>";
  } catch (err) { console.error("sensores:", err); }

  try {
    var a = document.getElementById("alerts");
    a.innerHTML = "";
    var al = data.alerts || [];
    if (!al.length) a.innerHTML = '<div class="note">Sin alertas activas.</div>';
    al.slice(0, 8).forEach(function (x) {
      a.innerHTML += '<div class="row"><span>' + (x.tipo || "") + " · " + (x.country || "") +
        "<small>" + (x.mensaje || "") + "</small></span>" +
        '<span class="badge ' + (x.nivel === "ALTO" ? "red" : "blue") + '">M ' + (x.mag || "") + "</span></div>";
    });
  } catch (err) { console.error("alertas:", err); }

  try {
    var p = document.getElementById("predict");
    p.innerHTML = "";
    (data.risk || []).slice(0, 8).forEach(function (r) {
      var pct = Math.round((r.prob_10y || 0) * 100);
      p.innerHTML += '<div class="row"><span>' + (r.country || "") + '</span><span class="badge ' +
        (pct > 40 ? "red" : pct > 15 ? "blue" : "green") + '">' + pct + "%</span></div>";
    });
  } catch (err) { console.error("riesgo:", err); }
}

/* ==========================================================
   7) TABLA: EN VIVO primero + fenómenos ordenados
   ========================================================== */
function renderTable(data) {
  try {
    var t = document.getElementById("pheno");
    var head = "<thead><tr><th>País</th><th>Lugar</th><th>Tipo</th><th>Año</th><th>Fecha</th><th>Hora</th><th>Mag</th><th>Prof</th><th>Impacto</th></tr></thead><tbody>";
    var live = (data.rt_events || []).slice(0, 30).map(function (e) {
      var d = new Date(e.time_utc);
      return "<tr><td>—</td><td>" + (e.place || "") + '</td><td><span class="badge red">🔴 EN VIVO</span></td><td>' +
        d.getUTCFullYear() + "</td><td>" + d.toLocaleDateString() + "</td><td>" + d.toLocaleTimeString() +
        "</td><td>" + e.mag + "</td><td>" + (e.depth_km != null ? Math.round(e.depth_km) : "") + "</td><td>—</td></tr>";
    }).join("");
    var phen = (data.phenomena || []).slice(0, 200).map(function (r) {
      return "<tr><td>" + (r.country || "") + "</td><td>" + (r.Lugar || "") + "</td><td>" + (r["Tipo de Fenómeno"] || "") +
        "</td><td>" + (r["Año"] || "") + "</td><td>" + (r["Día y Mes"] || "") + "</td><td>" + (r["Hora Local / (UTC)"] || "") +
        "</td><td>" + (r["Magnitud(es)"] || "") + "</td><td>" + (r["Profundidad (km)"] != null ? r["Profundidad (km)"] : "") +
        "</td><td>" + (r["Impacto / Comportamiento"] || "") + "</td></tr>";
    }).join("");
    t.innerHTML = head + live + phen + "</tbody>";
  } catch (err) { console.error("tabla:", err); }
}

/* ==========================================================
   8) PREDICCIONES
   ========================================================== */
function renderForecast(data) {
  try {
    var fc = document.getElementById("forecast");
    fc.innerHTML = "";
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var fut = (data.forecasts || []).filter(function (f) {
      var d = new Date(f.fecha_estimada);
      return !isNaN(d.getTime()) && d >= today;
    }).sort(function (a, b) { return new Date(a.fecha_estimada) - new Date(b.fecha_estimada); }).slice(0, 12);
    if (!fut.length) { fc.innerHTML = '<div class="note">📭 Sin predicciones futuras.</div>'; return; }
    fut.forEach(function (f) {
      var d = new Date(f.fecha_estimada);
      fc.innerHTML += '<div class="pred"><b>📍 ' + (f.country || "") + "</b> " +
        '<span class="badge ' + (f.dano === "ALTO" ? "red" : f.dano === "MEDIO" ? "blue" : "green") + '">' + f.dano + "</span>" +
        '<span class="f">' + (f.tipo || "") + " · " + (f.place || "") + "</span>" +
        '<span class="f">📅 ' + d.toLocaleDateString() + " ± " + (f.ventana_dias != null ? f.ventana_dias : "-") + " d</span>" +
        '<span class="f">📊 M' + (f.mag_lo != null ? f.mag_lo : "-") + "–M" + (f.mag_hi != null ? f.mag_hi : "-") +
        " · ⬇ " + (f.profundidad_km != null ? f.profundidad_km : "-") + " km</span>" +
        '<span class="f">🎯 ' + Math.round((f.probabilidad || 0) * 100) + "% · " + (f.confianza || "-") + "</span></div>";
    });
  } catch (err) { console.error("predicciones:", err); }
}

/* ==========================================================
   9) GRÁFICOS
   ========================================================== */
function renderCharts(data) {
  try {
    var all = (data.events || []).concat(data.rt_events || []);
    var mags = all.filter(function (e) { return e.mag != null; }).map(function (e) { return e.mag; });
    var bins = [6, 6.5, 7, 7.5, 8, 8.5, 9, 10];
    mkChart("ch_mag", bins.slice(0, -1).map(function (b) { return "M" + b; }),
      bins.slice(0, -1).map(function (b, i) {
        return mags.filter(function (m) { return m >= b && m < bins[i + 1]; }).length;
      }), "bar");
  } catch (err) { console.error("graf mag:", err); }

  try {
    var years = {};
    (data.events || []).forEach(function (e) { var y = (e.time_utc || "").slice(0, 4); if (y) years[y] = (years[y] || 0) + 1; });
    var ys = Object.keys(years).sort().slice(-30);
    mkChart("ch_year", ys, ys.map(function (y) { return years[y]; }), "line");
  } catch (err) { console.error("graf año:", err); }

  try {
    mkChart("ch_kp", ((data.magnetic && data.magnetic.kp_series) || []).map(function (k) { return (k.t || "").slice(11, 16); }),
      ((data.magnetic && data.magnetic.kp_series) || []).map(function (k) { return k.kp; }), "line");
  } catch (err) { console.error("graf kp:", err); }
}

function mkChart(id, labels, dataArr, type) {
  try {
    var el = document.getElementById(id);
    if (!el) return;
    if (CH[id]) CH[id].destroy();
    CH[id] = new Chart(el, {
      type: type,
      data: { labels: labels, datasets: [{ data: dataArr, borderColor: "#a29bfe", backgroundColor: "rgba(162,155,254,.3)", tension: 0.3 }] },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: "#8fa1c0" }, grid: { color: "#23304d" } },
          y: { ticks: { color: "#8fa1c0" }, grid: { color: "#23304d" } }
        }
      }
    });
  } catch (err) { console.error("mkChart " + id + ":", err); }
}

/* ==========================================================
   10) CIELO: ISS + satélites + debris + lanzamientos
   ========================================================== */
function renderSky() {
  try {
    var el = document.getElementById("iss_live");
    if (SKY.iss) {
      el.innerHTML =
        '<div class="row"><span>Lat/Lon</span><span class="badge blue">' + (+SKY.iss.latitude).toFixed(2) + ", " + (+SKY.iss.longitude).toFixed(2) + "</span></div>" +
        '<div class="row"><span>Altitud</span><span class="badge green">' + Math.round(SKY.iss.altitude_km || 0) + " km</span></div>" +
        '<div class="row"><span>Velocidad</span><span class="badge green">' + Math.round(SKY.iss.velocity_kmh || 0).toLocaleString() + " km/h</span></div>";
    } else el.innerHTML = '<div class="note">Sin datos ISS.</div>';
  } catch (err) { console.error("iss:", err); }

  try {
    G.sats.clearLayers(); MINI_SATS.clearLayers();
    (SKY.satellites || []).forEach(function (s) {
      if (s.latitude == null || s.longitude == null) return;
      var col = s.decaying ? "#ff4d4d" : s.military ? "#2ecc71" : s.type === "deb" ? "#e6ecf7" : "#3aa0ff";
      L.circleMarker([+s.latitude, +s.longitude], { radius: 3, color: col, fillColor: col, fillOpacity: 0.9, weight: 1 })
        .bindTooltip((s.flag || "") + " " + s.name + "<br>Alt " + Math.round(s.altitude_km || 0) + " km").addTo(G.sats);
      L.circleMarker([+s.latitude, +s.longitude], { radius: 2, color: col, fillOpacity: 0.9, weight: 1 }).addTo(MINI_SATS);
    });
    (SKY.launches || []).forEach(function (l) {
      if (l.lat == null || l.lon == null) return;
      L.marker([+l.lat, +l.lon], { icon: L.divIcon({ className: "", iconSize: [16, 16], html: '<div style="font-size:13px">🚀</div>' }) })
        .bindTooltip("🚀 " + (l.name || "")).addTo(MINI_SATS);
    });
    if (SKY.iss) {
      var la = +SKY.iss.latitude, lo = +SKY.iss.longitude;
      L.circleMarker([la, lo], { radius: 5, color: "#ff9f43", fillColor: "#ff9f43", fillOpacity: 1, weight: 2 }).addTo(G.sats);
      if (issTrail.length && Math.abs(lo - issTrail[issTrail.length - 1][1]) > 180) issTrail = [];
      issTrail.push([la, lo]);
      if (issTrail.length > 400) issTrail.shift();
      if (issTrailLine) minimap.removeLayer(issTrailLine);
      issTrailLine = L.polyline(issTrail, { color: "#ff9f43", weight: 1, opacity: 0.8 }).addTo(minimap);
    }
  } catch (err) { console.error("satélites mapa:", err); }

  try {
    var sl = document.getElementById("sat_list");
    sl.innerHTML = "";
    (SKY.satellites || []).slice(0, 40).forEach(function (s) {
      sl.innerHTML += '<div class="row"><span>' + (s.flag || "") + " " + (s.name || "") + '</span><span class="badge ' +
        (s.type === "deb" ? "gray" : s.military ? "green" : "blue") + '">' + Math.round(s.altitude_km || 0) + " km</span></div>";
    });
    var dl = document.getElementById("debris_list");
    dl.innerHTML = "";
    (SKY.satellites || []).filter(function (s) { return s.type === "deb" || s.decaying; }).slice(0, 30).forEach(function (s) {
      dl.innerHTML += '<div class="row"><span>' + (s.name || "") + '</span><span class="badge ' + (s.decaying ? "red" : "gray") + '">' +
        (s.decaying ? "REENTRA" : Math.round(s.altitude_km || 0) + " km") + "</span></div>";
    });
    (SKY.reentries || []).slice(0, 5).forEach(function (r) {
      dl.innerHTML += '<div class="row"><span>💥 ' + (r.name || "") + '</span><span class="badge gray">' + (r.ts || "").slice(5, 10) + "</span></div>";
    });
  } catch (err) { console.error("listas cielo:", err); }
}

/* ==========================================================
   11) ESPACIO: gauges reales + ozono + anomalías + listas
   ========================================================== */
function renderSpace() {
  try {
    var extra = SPACE.extra || {};
    var g = document.getElementById("sw_gauges");
    g.innerHTML = "";
    (extra.indicators || []).forEach(function (i) {
      g.innerHTML += '<div class="row"><span>' + i.name + '</span><span class="badge ' + i.color + '">' +
        (i.value != null ? i.value : "-") + " " + (i.unit || "") + "</span></div>";
    });
    mkChart("ch_xray", (extra.xray_series || []).map(function (x) { return (x.t || "").slice(11, 16); }),
      (extra.xray_series || []).map(function (x) { return x.v; }), "line");
  } catch (err) { console.error("gauges:", err); }

  try {
    var oz = document.getElementById("ozone_card");
    oz.innerHTML = SPACE.ozone ?
      '<div class="row"><span>Área ozono</span><span class="badge ' + (SPACE.ozone.area_mkm2 > 22 ? "red" : "blue") + '">' +
      SPACE.ozone.area_mkm2 + " M km²</span></div>" : '<div class="note">Sin datos de ozono.</div>';
  } catch (err) { console.error("ozono:", err); }

  try {
    var an = document.getElementById("anomaly_card");
    an.innerHTML = "";
    if (DATA) {
      var now = Date.now(), by = {}, hist = {};
      (DATA.events || []).forEach(function (e) {
        var d = (now - new Date(e.time_utc)) / 86400000;
        var c = e.country || "-";
        if (d <= 730) hist[c] = (hist[c] || 0) + 1;
        if (d <= 7) by[c] = (by[c] || 0) + 1;
      });
      Object.keys(by).map(function (c) {
        var avg = (hist[c] || 1) / 104;
        var pct = Math.round(((by[c] - avg) / avg) * 100);
        return { c: c, w: by[c], pct: pct };
      }).sort(function (a, b) { return b.w - a.w; }).slice(0, 6).forEach(function (x) {
        var cls = x.pct > 50 ? "red" : x.pct > 20 ? "blue" : "green";
        an.innerHTML += '<div class="row"><span>' + x.c + ' <small>' + x.w + ' sismos/7d</small></span><span class="badge ' + cls + '">' +
          (x.pct > 0 ? "+" : "") + x.pct + "% vs prom.</span></div>";
      });
    }
  } catch (err) { console.error("anomalías:", err); }

  try {
    var sl2 = document.getElementById("solar_list");
    sl2.innerHTML = "";
    (SPACE.orbits || []).forEach(function (o) {
      var last = (o.points || []).slice(-1)[0];
      var r = last ? Math.sqrt(last[0] * last[0] + last[1] * last[1]).toFixed(2) : "-";
      sl2.innerHTML += '<div class="row"><span>☄️ ' + (o.name || "") + '</span><span class="badge blue">' + r + " UA</span></div>";
    });
    if (!(SPACE.orbits || []).length) sl2.innerHTML = '<div class="note">Sin trayectorias Horizons.</div>';
  } catch (err) { console.error("solar list:", err); }

  try {
    var nl = document.getElementById("neo_list");
    nl.innerHTML = "";
    (SKY.asteroids || []).slice(0, 12).forEach(function (a) {
      nl.innerHTML += '<div class="row"><span>☄️ ' + (a.name || "") + '</span><span class="badge ' +
        (a.hazardous ? "red" : "green") + '">' + ((a.distance_km || 0) / 1.5e8).toFixed(3) + " UA</span></div>";
    });
    (SPACE.sentry || []).slice(0, 5).forEach(function (s) {
      nl.innerHTML += '<div class="row"><span>⚠️ ' + (s.name || "") + '</span><span class="badge gray">P ' +
        (s.ps != null ? (+s.ps).toExponential(1) : "-") + "</span></div>";
    });
  } catch (err) { console.error("neo list:", err); }
}

/* ==========================================================
   12) ANIMACIONES CANVAS
   ========================================================== */
function spaceLoop() {
  drawSpaceWeather();
  drawDebris();
  drawSolar();
  drawNeo();
  requestAnimationFrame(spaceLoop);
}

function drawSpaceWeather() {
  var cv = document.getElementById("sw_anim");
  if (!cv) return;
  var ctx = cv.getContext("2d"), W = cv.width = cv.clientWidth, H = cv.height = cv.clientHeight;
  var w = SPACE.weather || {}, k = w.kp || 1, level = w.level || "NORMAL";
  swT += 0.016;
  ctx.clearRect(0, 0, W, H);
  var g2 = ctx.createRadialGradient(30, H / 2, 2, 30, H / 2, 30);
  g2.addColorStop(0, "#ffd166"); g2.addColorStop(1, "rgba(255,159,67,0)");
  ctx.fillStyle = g2; ctx.beginPath(); ctx.arc(30, H / 2, 30, 0, 7); ctx.fill();
  ctx.fillStyle = "#ff9f43"; ctx.beginPath(); ctx.arc(30, H / 2, 12 + k, 0, 7); ctx.fill();
  var sp = ((w.wind_speed || 400) / 100) + k;
  ctx.fillStyle = level === "TORMENTA" ? "#ff4d4d" : level === "ACTIVO" ? "#ffd166" : "#3aa0ff";
  for (var i = 0; i < 40 + k * 15; i++) {
    ctx.fillRect(((i * 53 + swT * sp * 60) % (W - 90)) + 50, (i * 37) % H, 2, 2);
  }
  ctx.fillStyle = "#3aa0ff"; ctx.beginPath(); ctx.arc(W - 40, H / 2, 8, 0, 7); ctx.fill();
  ctx.strokeStyle = level === "TORMENTA" ? "#ff4d4d" : "#2ecc71"; ctx.lineWidth = 2;
  var c = Math.max(10, 30 - k * 3);
  ctx.beginPath(); ctx.ellipse(W - 40, H / 2, c + 10, c + 16, 0, -1.2, 1.2); ctx.stroke();
}

function drawDebris() {
  var cv = document.getElementById("debris_radar");
  if (!cv) return;
  var ctx = cv.getContext("2d"), W = cv.width = cv.clientWidth, H = cv.height = cv.clientHeight;
  ctx.clearRect(0, 0, W, H);
  DEBRIS_PTS = [];
  ctx.save();
  ctx.translate(W / 2 + DEBRIS_VIEW.ox, H / 2 + DEBRIS_VIEW.oy);
  ctx.scale(DEBRIS_VIEW.scale, DEBRIS_VIEW.scale);
  var R = Math.min(W, H) / 2 - 10;
  ctx.fillStyle = "#3aa0ff"; ctx.beginPath(); ctx.arc(0, 0, R * 0.25, 0, 7); ctx.fill();
  [0.45, 0.7, 0.95].forEach(function (rr) {
    ctx.strokeStyle = "#23304d"; ctx.beginPath(); ctx.arc(0, 0, R * rr, 0, 7); ctx.stroke();
  });
  debA += 0.02;
  ctx.strokeStyle = "#2ecc71"; ctx.beginPath(); ctx.moveTo(0, 0);
  ctx.lineTo(Math.cos(debA) * R, Math.sin(debA) * R); ctx.stroke();
  ctx.font = "9px sans-serif";
  (SKY.satellites || []).slice(0, 60).forEach(function (s, i) {
    if (s.latitude == null || s.longitude == null) return;
    var alt = s.altitude_km || 500;
    var rr = alt < 2000 ? 0.45 : alt < 20000 ? 0.7 : 0.95;
    var ang = (s.longitude + 180) / 360 * 2 * Math.PI;
    var x = Math.cos(ang) * R * rr, y = Math.sin(ang) * R * rr;
    var col = s.decaying ? "#ff4d4d" : s.military ? "#2ecc71" : s.type === "deb" ? "#e6ecf7" : "#3aa0ff";
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 2, 0, 7); ctx.fill();
    if (i < 15) { ctx.fillStyle = "#8fa1c0"; ctx.fillText((s.name || "").slice(0, 14), x + 4, y - 3); }
    DEBRIS_PTS.push({
      x: W / 2 + DEBRIS_VIEW.ox + x * DEBRIS_VIEW.scale,
      y: H / 2 + DEBRIS_VIEW.oy + y * DEBRIS_VIEW.scale,
      info: (s.flag || "") + " <b>" + (s.name || "") + "</b><br>Alt " + Math.round(alt) + " km<br>" +
        (s.military ? "MILITAR" : s.type === "deb" ? "BASURA ESPACIAL" : "civil")
    });
  });
  ctx.restore();
}

function drawSolar() {
  var cv = document.getElementById("solar_map");
  if (!cv) return;
  var ctx = cv.getContext("2d"), W = cv.width = cv.clientWidth, H = cv.height = cv.clientHeight;
  ctx.clearRect(0, 0, W, H);
  SOLAR_PTS = [];
  ctx.save();
  ctx.translate(W / 2 + SOLAR_VIEW.ox, H / 2 + SOLAR_VIEW.oy);
  ctx.scale(SOLAR_VIEW.scale, SOLAR_VIEW.scale);
  var S = Math.min(W, H) / 2 / 1.8;
  ctx.fillStyle = "#ffd166"; ctx.beginPath(); ctx.arc(0, 0, 8, 0, 7); ctx.fill();
  var days = Date.now() / 86400000;
  [["Tierra", 1, 1, "#3aa0ff"], ["Marte", 1.52, 1.88, "#8fa1c0"]].forEach(function (p) {
    ctx.strokeStyle = "#23304d"; ctx.beginPath(); ctx.arc(0, 0, p[1] * S, 0, 7); ctx.stroke();
    var a = 2 * Math.PI * (days / (p[2] * 365.25));
    ctx.fillStyle = p[3]; ctx.beginPath(); ctx.arc(Math.cos(a) * p[1] * S, Math.sin(a) * p[1] * S, 3, 0, 7); ctx.fill();
  });
  ctx.font = "10px sans-serif";
  (SPACE.orbits || []).forEach(function (o) {
    ctx.strokeStyle = "#2ecc71"; ctx.beginPath();
    (o.points || []).forEach(function (pt, i) {
      var x = pt[0] * S, y = -pt[1] * S;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    var last = (o.points || []).slice(-1)[0];
    if (last) {
      var lx = last[0] * S, ly = -last[1] * S;
      ctx.fillStyle = "#2ecc71"; ctx.beginPath(); ctx.arc(lx, ly, 4, 0, 7); ctx.fill();
      if (last.length >= 4) {
        var vx = last[2], vy = -last[3], m = Math.sqrt(vx * vx + vy * vy) || 1;
        ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(lx + vx / m * 14, ly + vy / m * 14); ctx.stroke();
      }
      ctx.fillStyle = "#e6ecf7"; ctx.fillText((o.name || "").slice(0, 14), lx + 6, ly - 4);
      SOLAR_PTS.push({
        x: W / 2 + SOLAR_VIEW.ox + lx * SOLAR_VIEW.scale,
        y: H / 2 + SOLAR_VIEW.oy + ly * SOLAR_VIEW.scale,
        info: "☄️ <b>" + (o.name || "") + "</b><br>Trayectoria real ±45 d (Horizons)"
      });
    }
  });
  ctx.restore();
}

function drawNeo() {
  var cv = document.getElementById("neo_radar");
  if (!cv) return;
  var ctx = cv.getContext("2d"), W = cv.width = cv.clientWidth, H = cv.height = cv.clientHeight;
  ctx.clearRect(0, 0, W, H);
  RADAR_PTS = [];
  ctx.save();
  ctx.translate(W / 2 + RADAR_VIEW.ox, H / 2 + RADAR_VIEW.oy);
  ctx.scale(RADAR_VIEW.scale, RADAR_VIEW.scale);
  var R = Math.min(W, H) / 2 - 10;
  [0.05, 0.1, 0.2, 0.3].forEach(function (d) {
    ctx.strokeStyle = "#23304d"; ctx.beginPath(); ctx.arc(0, 0, (d / 0.3) * R, 0, 7); ctx.stroke();
  });
  neoA += 0.02;
  ctx.strokeStyle = "#2ecc71"; ctx.beginPath(); ctx.moveTo(0, 0);
  ctx.lineTo(Math.cos(neoA) * R, Math.sin(neoA) * R); ctx.stroke();
  ctx.font = "9px sans-serif";
  (SKY.asteroids || []).slice(0, 14).forEach(function (a, i) {
    var ang = (i * 2.39996) % (2 * Math.PI);
    var rr = Math.min(1, ((a.distance_km || 0) / 1.5e8) / 0.3) * R;
    var x = Math.cos(ang) * rr, y = Math.sin(ang) * rr;
    ctx.fillStyle = a.hazardous ? "#ff4d4d" : "#ffd166";
    ctx.beginPath(); ctx.arc(x, y, 3, 0, 7); ctx.fill();
    ctx.fillStyle = "#8fa1c0"; ctx.fillText((a.name || "").slice(0, 14), x + 4, y - 3);
    RADAR_PTS.push({
      x: W / 2 + RADAR_VIEW.ox + x * RADAR_VIEW.scale,
      y: H / 2 + RADAR_VIEW.oy + y * RADAR_VIEW.scale,
      info: "☄️ <b>" + (a.name || "") + "</b><br>" + ((a.distance_km || 0) / 1.5e8).toFixed(3) + " UA<br>" +
        (a.hazardous ? "🔴 Potencialmente peligroso" : "🟢 Pasa de largo")
    });
  });
  ctx.fillStyle = "#3aa0ff"; ctx.beginPath(); ctx.arc(0, 0, 4, 0, 7); ctx.fill();
  ctx.restore();
}

/* ==========================================================
   13) CONTROLES DE CAPAS Y RANGO
   ========================================================== */
try {
  [["ly_plates", ["plates"]], ["ly_fallas", ["fallas", "falla_labels", "zonas"]],
   ["ly_quakes", ["quakes"]], ["ly_volc", ["volc"]], ["ly_magma", ["magma"]],
   ["ly_sats", ["sats"]]].forEach(function (pair) {
    var el = document.getElementById(pair[0]);
    if (!el) return;
    el.onchange = function (e) {
      pair[1].forEach(function (k) {
        if (e.target.checked) G[k].addTo(map); else map.removeLayer(G[k]);
      });
    };
  });
} catch (err) { console.error("toggles:", err); }

try {
  document.querySelectorAll('input[name="qrange"]').forEach(function (r) {
    r.onchange = function (e) { Q_RANGE = e.target.value; if (DATA) render(DATA); };
  });
} catch (err) { console.error("qrange:", err); }

/* ==========================================================
   14) CLIC EN MAPA → datos reales de la zona (sin API extra)
   ========================================================== */
map.on("click", function (e) {
  try {
    var la = e.latlng.lat, lo = e.latlng.lng;
    var now = Date.now(), q30 = 0, maxM = null;
    (DATA && DATA.events || []).concat(DATA && DATA.rt_events || []).forEach(function (ev) {
      if ((now - new Date(ev.time_utc)) / 86400000 <= 30 &&
          haversineKm(la, lo, +ev.latitude, +ev.longitude) <= 300) {
        q30++;
        if (ev.mag != null && (maxM == null || ev.mag > maxM)) maxM = ev.mag;
      }
    });
    var bv = null, bd = 1e18;
    (DATA && DATA.volcanoes || []).forEach(function (v) {
      var d = haversineKm(la, lo, +v.lat, +v.lon);
      if (d < bd) { bd = d; bv = v; }
    });
    var bf = null, fd = 1e18;
    (DATA && DATA.fallas || []).forEach(function (f) {
      var c = (f.coords || [])[0];
      if (!c) return;
      var d = haversineKm(la, lo, c[0], c[1]);
      if (d < fd) { fd = d; bf = f; }
    });
    L.popup({ maxWidth: 320 }).setLatLng(e.latlng).setContent(
      "<b>📍 Zona " + la.toFixed(1) + ", " + lo.toFixed(1) + "</b><br>" +
      "🔴 Sismos 30d/300km: <b>" + q30 + "</b> (máx M" + (maxM != null ? maxM : "-") + ")<br>" +
      "🌋 Volcán: <b>" + (bv ? bv.name : "-") + "</b> (" + (bv ? Math.round(bd) : "-") + " km)<br>" +
      "⚡ Falla: <b>" + (bf ? bf.nombre : "-") + "</b> (" + (bf ? Math.round(fd) : "-") + " km, Mw " + (bf ? bf.mw_max_estimado : "-") + ")"
    ).openOn(map);
  } catch (err) { console.error("click:", err); }
});

/* ==========================================================
   15) ARRANQUE + INTERVALOS (tiempo real)
   ========================================================== */
load(); loadSky(); loadSpace();
setInterval(load, 60000);       // sismos/fenómenos cada 60 s (antes que nadie)
setInterval(loadSky, 10000);    // satélites/ISS cada 10 s
setInterval(loadSpace, 60000);  // espacio cada 60 s
spaceLoop();
console.log("=== Dashboard iniciado ===");
</script>
</body>
</html>
"""