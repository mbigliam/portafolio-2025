"""
Punto de Entrada para ejecución modular: `python -m app`
"""
import sys
from app.application import JarvisApplication

if __name__ == "__main__":
    app = JarvisApplication()
    sys.exit(app.run())