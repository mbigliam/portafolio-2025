#!/usr/bin/env python3
"""
IA Security Gateway - Verificar Instalación
Diagnostic script to verify file replacements and backend connectivity
"""

import os
import sys
import requests
import json
from pathlib import Path

def check_files():
    """Verify that fixed files exist and are correctly replaced"""
    print("\n" + "="*60)
    print("📁 VERIFICANDO ARCHIVOS")
    print("="*60)

    base_path = Path("public")

    files_to_check = {
        "index.html": "Frontend HTML",
        "app.js": "Frontend JavaScript"
    }

    all_good = True

    for filename, description in files_to_check.items():
        file_path = base_path / filename
        if file_path.exists():
            size = file_path.stat().st_size
            # Check if it's the fixed version (should have specific markers)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if filename == "index.html":
                # Check for fixed version markers
                if "Prueba de Seguridad" in content and "app.js" in content:
                    print(f"✅ {filename} ({description}): {size} bytes - CORRECTO")
                else:
                    print(f"⚠️  {filename} ({description}): {size} bytes - POSIBLEMENTE INCORRECTO")
                    all_good = False
            elif filename == "app.js":
                # Check for fixed version markers
                if "API_BASE = 'http://localhost:8000/api'" in content and "DOMContentLoaded" in content:
                    print(f"✅ {filename} ({description}): {size} bytes - CORRECTO")
                else:
                    print(f"⚠️  {filename} ({description}): {size} bytes - POSIBLEMENTE INCORRECTO")
                    all_good = False
        else:
            print(f"❌ {filename} ({description}): NO ENCONTRADO")
            all_good = False

    return all_good

def check_backend():
    """Test backend connectivity and endpoints"""
    print("\n" + "="*60)
    print("🔌 VERIFICANDO BACKEND")
    print("="*60)

    api_base = "http://localhost:8000"
    timeout = 5

    tests = [
        ("GET", f"{api_base}/api/status", "Status Endpoint"),
        ("GET", f"{api_base}/api/traffic-stats", "Traffic Stats Endpoint"),
        ("GET", f"{api_base}/api/compliance", "Compliance Endpoint"),
    ]

    all_good = True

    for method, url, description in tests:
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
                status_code = response.status_code

                if status_code == 200:
                    print(f"✅ {description}: {status_code} OK")
                    try:
                        data = response.json()
                        print(f"   Respuesta: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        pass
                else:
                    print(f"⚠️  {description}: {status_code} (expected 200)")
                    all_good = False
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}: NO PUEDE CONECTAR (backend no está corriendo?)")
            all_good = False
        except requests.exceptions.Timeout:
            print(f"❌ {description}: TIMEOUT (backend no responde)")
            all_good = False
        except Exception as e:
            print(f"❌ {description}: ERROR - {str(e)}")
            all_good = False

    return all_good

def check_frontend():
    """Test that frontend is served correctly"""
    print("\n" + "="*60)
    print("🌐 VERIFICANDO FRONTEND")
    print("="*60)

    try:
        response = requests.get("http://localhost:8000", timeout=5)

        if response.status_code == 200:
            if "index.html" in response.text or "Prueba de Seguridad" in response.text:
                print(f"✅ Frontend servido correctamente: {len(response.text)} bytes")

                # Check for key elements
                checks = [
                    ("promptInput", "Textarea para prompts"),
                    ("sendBtn", "Botón de envío"),
                    ("app.js", "Script de aplicación"),
                ]

                for elem_id, desc in checks:
                    if elem_id in response.text:
                        print(f"   ✅ Elemento encontrado: {desc} ({elem_id})")
                    else:
                        print(f"   ❌ Elemento NO encontrado: {desc} ({elem_id})")

                return True
            else:
                print(f"❌ Frontend no parece ser la versión correcta")
                return False
        else:
            print(f"❌ Frontend respondió con status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ NO PUEDE CONECTAR AL FRONTEND (backend no está corriendo)")
        return False
    except Exception as e:
        print(f"❌ ERROR al verificar frontend: {str(e)}")
        return False

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   IA SECURITY GATEWAY - VERIFICADOR DE INSTALACIÓN        ║")
    print("║   Diagnostic Tool v1.0                                    ║")
    print("╚════════════════════════════════════════════════════════════╝")

    # Run checks
    files_ok = check_files()
    frontend_ok = check_frontend()
    backend_ok = check_backend()

    # Summary
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)

    if files_ok:
        print("✅ Archivos: Todos en lugar correcto")
    else:
        print("❌ Archivos: Revisar reemplazos de archivos")

    if frontend_ok:
        print("✅ Frontend: Sirviendo correctamente")
    else:
        print("❌ Frontend: Verificar que backend esté corriendo")

    if backend_ok:
        print("✅ Backend: Respondiendo en todas las rutas")
    else:
        print("❌ Backend: No está respondiendo - iniciar con:")
        print("   py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

    print("\n" + "="*60)

    if files_ok and frontend_ok and backend_ok:
        print("✅ ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\nPasos siguientes:")
        print("1. Abre http://localhost:8000 en tu navegador")
        print("2. Abre la consola (F12)")
        print("3. Intenta con el botón 'Datos Públicos (Permitido)'")
        print("4. Verifica la consola para ver logs de debug")
        return 0
    else:
        print("❌ PROBLEMAS DETECTADOS - Ver arriba para detalles")
        return 1

if __name__ == "__main__":
    sys.exit(main())
