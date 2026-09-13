"""
Módulo de Gestión de Configuración para JARVIS.
Carga y valida archivos YAML con valores por defecto seguros.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict
import yaml


@dataclass
class UIConfig:
    window_title: str = "J.A.R.V.I.S. // Desktop Core Interface"
    theme: str = "hologram_cyan"
    fullscreen: bool = False
    width: int = 1280
    height: int = 800
    fps: int = 60
    particle_count: int = 60
    glow_intensity: float = 1.0


@dataclass
class SystemConfig:
    name: str = "JARVIS"
    version: str = "1.0.0"
    language: str = "es-ES"
    debug_mode: bool = True
    start_with_windows: bool = False


@dataclass
class AppConfig:
    system: SystemConfig = field(default_factory=SystemConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    raw_data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Path | str | None = None) -> "AppConfig":
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
        else:
            config_path = Path(config_path)

        if not config_path.exists():
            return cls()

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        sys_data = data.get("system", {})
        ui_data = data.get("ui", {})

        return cls(
            system=SystemConfig(
                name=sys_data.get("name", "JARVIS"),
                version=sys_data.get("version", "1.0.0"),
                language=sys_data.get("language", "es-ES"),
                debug_mode=sys_data.get("debug_mode", True),
                start_with_windows=sys_data.get("start_with_windows", False),
            ),
            ui=UIConfig(
                window_title=ui_data.get("window_title", "J.A.R.V.I.S. // Core"),
                theme=ui_data.get("theme", "hologram_cyan"),
                fullscreen=ui_data.get("fullscreen", False),
                width=ui_data.get("width", 1280),
                height=ui_data.get("height", 800),
                fps=ui_data.get("fps", 60),
                particle_count=ui_data.get("particle_count", 60),
                glow_intensity=ui_data.get("glow_intensity", 1.0),
            ),
            raw_data=data,
        )