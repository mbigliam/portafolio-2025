"""
Coordinador de JARVIS con AI Engine Integrado.
"""
import logging
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from ai.router import AIRouter
from app.config import AppConfig
from core.state import StateMachine, SystemState
from ui.main_window import MainWindow
from voice.voice_engine import VoiceEngine


class JarvisApplication:
    def __init__(self, config_path: Path | str | None = None):
        self._setup_logging()
        self.config = AppConfig.load(config_path)
        self.state_machine = StateMachine(initial_state=SystemState.STARTING)
        self.ai_router = AIRouter(self.config)
        self.voice_engine = VoiceEngine(self.state_machine, self.ai_router, language=self.config.system.language)
        self.qt_app: QApplication | None = None
        self.main_window: MainWindow | None = None

    def _setup_logging(self) -> None:
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "application.log"

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        def exception_hook(exctype, value, traceback):
            logging.error("Excepción no capturada:", exc_info=(exctype, value, traceback))
            sys.__excepthook__(exctype, value, traceback)

        sys.excepthook = exception_hook

    def run(self) -> int:
        logging.info(f"Iniciando {self.config.system.name} con Cerebro de IA...")
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.main_window = MainWindow(self.state_machine, voice_engine=self.voice_engine)

        self.state_machine.transition_to(SystemState.IDLE, reason="Sistema listo para interactuar")
        self.main_window.show()

        self.voice_engine.start()

        exit_code = self.qt_app.exec()
        logging.info("JARVIS detenido correctamente.")
        return exit_code