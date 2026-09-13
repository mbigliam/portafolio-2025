# -*- coding: utf-8 -*-
"""Test de sensores geofísicos"""
import requests
from datetime import datetime, timedelta, timezone
import numpy as np

USGS_GEOMAG_URL = "https://geomag.usgs.gov/ws/data/"
SWPC_KP_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

print("=" * 60)
print("TEST DE APIs DE SENSORES GEOFÍSICOS")
print("=" * 60)

# Test 1: Kp Index
print("\n1️⃣ Probando NOAA SWPC Kp Index...")
try:
    r = requests.get(SWPC_KP_URL, timeout=30)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Datos obtenidos: {len(data)} registros")
        if data:
            last = data[-1]
            print(f"   Último Kp: {last.get('kp')}")
    else:
        print(f"   ❌ Error: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Excepción: {e}")

# Test 2: USGS Geomagnetism
print("\n2️⃣ Probando USGS Geomagnetism (observatorio BOU)...")
try:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = {
        "id": "BOU",
        "format": "json",
        "elements": "H",
        "starttime": start,
        "endtime": end,
        "sampling_period": 3600
    }
    
    print(f"   URL: {USGS_GEOMAG_URL}")
    print(f"   Parámetros: {params}")
    
    r = requests.get(USGS_GEOMAG_URL, params=params, timeout=30)
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Respuesta recibida")
        
        # Verificar estructura
        if isinstance(data, dict):
            print(f"   Tipo: dict con keys: {list(data.keys())[:5]}")
            if "timeseries" in data:
                ts = data["timeseries"]
                if isinstance(ts, dict):
                    for key in list(ts.keys())[:3]:
                        vals = ts[key]
                        if isinstance(vals, list):
                            print(f"   {key}: {len(vals)} valores")
                            if vals:
                                print(f"      Primer valor: {vals[0]}")
        elif isinstance(data, list):
            print(f"   Tipo: lista con {len(data)} elementos")
            if data:
                print(f"   Primer elemento: {data[0]}")
    else:
        print(f"   ❌ Error: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Excepción: {type(e).__name__}: {e}")

# Test 3: F10.7 Radio Flux
print("\n3️⃣ Probando NOAA F10.7 Radio Flux...")
try:
    r = requests.get("https://services.swpc.noaa.gov/json/f107_cm_flux.json", timeout=30)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Datos obtenidos: {len(data)} registros")
        if data:
            print(f"   Último: {data[-1]}")
except Exception as e:
    print(f"   ❌ Excepción: {e}")

# Test 4: GOES X-ray
print("\n4️⃣ Probando NOAA GOES X-ray...")
try:
    r = requests.get("https://services.swpc.noaa.gov/json/goes/primary/xray-1-day.json", timeout=30)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Datos obtenidos: {len(data)} registros")
        if data:
            print(f"   Último flux: {data[-1].get('flux')}")
except Exception as e:
    print(f"   ❌ Excepción: {e}")

print("\n" + "=" * 60)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 60)