"""
Paneles Laterales de la Interfaz Holográfica HUD (Sin Captura Indebida de Foco de Teclado).
"""
import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.event_bus import Event, EventType, global_event_bus
from core.state import SystemState
from ui.themes import HologramTheme


class FuturisticPanel(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(10, 20, 36, 170);
                border: 1px solid rgba(0, 229, 255, 70);
                border-radius: 8px;
            }}
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 12, 14, 12)
        self.layout.setSpacing(8)

        self.lbl_title = QLabel(f"// {title.upper()}")
        self.lbl_title.setStyleSheet(f"""
            color: {HologramTheme.TEXT_ACCENT};
            font-family: '{HologramTheme.FONT_MONO}';
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1px;
            border: none;
            background: transparent;
        """)
        self.layout.addWidget(self.lbl_title)


class TelemetryPanel(FuturisticPanel):
    def __init__(self, parent=None):
        super().__init__("SISTEMA // TELEMETRÍA", parent)

        self.lbl_cpu = QLabel("CPU: 0.0%")
        self.bar_cpu = self._create_bar()

        self.lbl_ram = QLabel("RAM: 0.0 GB / 0.0 GB (0%)")
        self.bar_ram = self._create_bar()

        self.lbl_disk = QLabel("DISCO C:\\: 0%")
        self.bar_disk = self._create_bar()

        self.lbl_proc = QLabel("PROCESOS ACTIVOS: 0")

        for lbl, bar in [
            (self.lbl_cpu, self.bar_cpu),
            (self.lbl_ram, self.bar_ram),
            (self.lbl_disk, self.bar_disk),
        ]:
            self._apply_label_style(lbl)
            self.layout.addWidget(lbl)
            self.layout.addWidget(bar)

        self._apply_label_style(self.lbl_proc)
        self.layout.addWidget(self.lbl_proc)

        self.lbl_voice_status = QLabel("VOZ: ACTIVA // WAKE WORD: 'JARVIS'")
        self._apply_label_style(self.lbl_voice_status)
        self.lbl_voice_status.setStyleSheet(f"color: #00ffcc; font-family: '{HologramTheme.FONT_MONO}'; font-size: 10.5px; border:none; background:transparent; font-weight:bold;")
        self.layout.addWidget(self.lbl_voice_status)

        psutil.cpu_percent(interval=None)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh_telemetry)
        self.timer.start(1000)
        self._refresh_telemetry()

    def _apply_label_style(self, lbl: QLabel):
        lbl.setStyleSheet(f"""
            color: {HologramTheme.TEXT_PRIMARY};
            font-family: '{HologramTheme.FONT_MONO}';
            font-size: 11px;
            border: none;
            background: transparent;
        """)

    def _create_bar(self) -> QProgressBar:
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setFixedHeight(8)
        bar.setTextVisible(False)
        bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(0, 50, 80, 120);
                border: 1px solid rgba(0, 229, 255, 40);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0055ff, stop:1 #00e5ff);
                border-radius: 3px;
            }
        """)
        return bar

    def _refresh_telemetry(self):
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            proc_count = len(psutil.pids())

            self.lbl_cpu.setText(f"CPU: {cpu:.1f}%")
            self.bar_cpu.setValue(int(cpu))

            ram_u = round(ram.used / (1024**3), 2)
            ram_t = round(ram.total / (1024**3), 2)
            self.lbl_ram.setText(f"RAM: {ram_u} GB / {ram_t} GB ({ram.percent:.1f}%)")
            self.bar_ram.setValue(int(ram.percent))

            self.lbl_disk.setText(f"DISCO C:\\: {disk.percent:.1f}%")
            self.bar_disk.setValue(int(disk.percent))

            self.lbl_proc.setText(f"PROCESOS ACTIVOS: {proc_count}")
        except Exception:
            pass


class ActivityPanel(FuturisticPanel):
    def __init__(self, parent=None):
        super().__init__("REGISTRO DE ACTIVIDAD // EVENTOS", parent)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        # DESACTIVAR FOCO PARA QUE NO BLOQUEE LA BARRA ESPACIADORA
        self.txt_log.setFocusPolicy(Qt.NoFocus)
        self.txt_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {HologramTheme.TEXT_SECONDARY};
                font-family: '{HologramTheme.FONT_MONO}';
                font-size: 10.5px;
                line-height: 1.4;
            }}
        """)
        self.layout.addWidget(self.txt_log)
        global_event_bus.subscribe(EventType.LOG_MESSAGE, self._on_log_message)

    def _on_log_message(self, event: Event):
        self.log(str(event.data))

    def log(self, message: str) -> None:
        self.txt_log.append(f"> {message}")
        sb = self.txt_log.verticalScrollBar()
        sb.setValue(sb.maximum())


class StateControlBar(QFrame):
    def __init__(self, on_change_callback, on_mic_callback, parent=None):
        super().__init__(parent)
        self.on_change = on_change_callback
        self.on_mic = on_mic_callback

        self.setStyleSheet("""
            QFrame {
                background-color: rgba(6, 15, 28, 220);
                border: 1px solid rgba(0, 229, 255, 60);
                border-radius: 10px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        self.btn_mic = QPushButton("🎙 HABLAR CON JARVIS [ESPACIO]")
        self.btn_mic.setFocusPolicy(Qt.NoFocus)
        self.btn_mic.setCursor(Qt.PointingHandCursor)
        self.btn_mic.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0055ff, stop:1 #00ffcc);
                color: #060a12;
                border: 1px solid #00e5ff;
                border-radius: 6px;
                padding: 7px 16px;
                font-family: 'Consolas';
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00ffcc;
                color: #000000;
            }
        """)
        self.btn_mic.clicked.connect(self.on_mic)
        layout.addWidget(self.btn_mic)

        layout.addSpacing(10)

        lbl = QLabel("TEST ESTADOS:")
        lbl.setStyleSheet(f"""
            color: {HologramTheme.TEXT_ACCENT};
            font-family: '{HologramTheme.FONT_MONO}';
            font-weight: bold;
            font-size: 11px;
            border: none;
            background: transparent;
        """)
        layout.addWidget(lbl)

        states = [
            ("IDLE [1]", SystemState.IDLE, "#00e5ff"),
            ("LISTEN [2]", SystemState.LISTENING, "#00ffaa"),
            ("THINK [3]", SystemState.THINKING, "#ffaa00"),
            ("SPEAK [4]", SystemState.SPEAKING, "#80f7ff"),
            ("EXEC [5]", SystemState.EXECUTING, "#d000ff"),
            ("ERROR [6]", SystemState.ERROR, "#ff2255"),
        ]

        for text, st, color in states:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0, 30, 60, 160);
                    color: {color};
                    border: 1px solid {color};
                    border-radius: 5px;
                    padding: 6px 10px;
                    font-family: '{HologramTheme.FONT_MONO}';
                    font-size: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: #000000;
                }}
            """)
            btn.clicked.connect(lambda checked=False, s=st: self.on_change(s))
            layout.addWidget(btn)