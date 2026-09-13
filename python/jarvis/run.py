"""
Script de Ejecución Directa: `python run.py`
"""
import sys
from app.application import JarvisApplication

if __name__ == "__main__":
    app = JarvisApplication()
    sys.exit(app.run())