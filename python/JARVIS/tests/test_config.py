import pytest
from app.config import AppConfig


def test_default_config_loading():
    config = AppConfig.load(config_path=None)
    assert config.system.name == "JARVIS"
    assert config.ui.fps == 60
    assert config.ui.theme == "hologram_cyan"