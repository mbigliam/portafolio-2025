"""
Módulo de Telemetría del Sistema Operativo Windows.
"""
from typing import Dict
import psutil


class SystemMonitor:
    """Proveedor utilitario de métricas de Windows."""

    @staticmethod
    def get_current_metrics() -> Dict[str, float]:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")

        return {
            "cpu_percent": float(cpu),
            "ram_percent": float(ram.percent),
            "ram_used_gb": round(ram.used / (1024**3), 2),
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "disk_percent": float(disk.percent),
            "processes_count": len(psutil.pids()),
        }