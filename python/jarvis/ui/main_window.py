"""
Ventana Principal de JARVIS con Foco Seguro y Barra Espaciadora Exclusiva para Voz.
"""
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QKeyEvent, QPainter
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from core.event_bus import EventType, global_event_bus
from core.state import StateMachine, SystemState
from ui.core_widget import HolographicCoreWidget
from ui.hud_panels import ActivityPanel, StateControlBar, TelemetryPanel
from ui.themes import HologramTheme


class MainWindow(QMainWindow):
    """Ventana principal HUD futurista para JARVIS."""

    def __init__(self, state_machine: StateMachine, voice_engine=None):
        super().__init__()
        self.state_machine = state_machine
        self.voice_engine = voice_engine

        self.setWindowTitle("J.A.R.V.I.S. // Desktop AI Interface")
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 18, 20, 16)
        main_layout.setSpacing(14)

        # 1. Header con Botón de Apagado (Sin foco de teclado)
        header_layout = QHBoxLayout()
        self.lbl_brand = QLabel("MARK VII // DESKTOP SYSTEM")
        self.lbl_brand.setStyleSheet(f"""
            color: {HologramTheme.TEXT_ACCENT};
            font-family: '{HologramTheme.FONT_MONO}';
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        self.lbl_status = QLabel(self.state_machine.current_state.label)
        self.lbl_status.setStyleSheet(f"""
            color: {HologramTheme.TEXT_PRIMARY};
            font-family: '{HologramTheme.FONT_MONO}';
            font-size: 12px;
            font-weight: bold;
        """)

        self.btn_exit = QPushButton("⏻ APAGAR [ESC]")
        self.btn_exit.setFocusPolicy(Qt.NoFocus)  # EVITA QUE LA BARRA ESPACIADORA LO ACCIONE
        self.btn_exit.setCursor(Qt.PointingHandCursor)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 30, 70, 40);
                color: #ff3366;
                border: 1px solid #ff3366;
                border-radius: 4px;
                padding: 4px 12px;
                font-family: 'Consolas';
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff3366;
                color: #ffffff;
            }
        """)
        self.btn_exit.clicked.connect(self._exit_system)

        header_layout.addWidget(self.lbl_brand)
        header_layout.addStretch()
        header_layout.addWidget(self.lbl_status)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.btn_exit)
        main_layout.addLayout(header_layout)

        # 2. Body
        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        self.panel_telemetry = TelemetryPanel()
        self.panel_telemetry.setFixedWidth(280)

        self.core_widget = HolographicCoreWidget()

        self.panel_activity = ActivityPanel()
        self.panel_activity.setFixedWidth(320)

        body_layout.addWidget(self.panel_telemetry)
        body_layout.addWidget(self.core_widget, stretch=1)
        body_layout.addWidget(self.panel_activity)
        main_layout.addLayout(body_layout, stretch=1)

        # 3. Footer Control Bar
        self.control_bar = StateControlBar(
            on_change_callback=self._on_user_request_state,
            on_mic_callback=self._on_mic_clicked,
        )
        main_layout.addWidget(self.control_bar)

        self.state_machine.add_listener(self._on_state_changed)

        self.panel_activity.log("JARVIS Kernel activo.")
        self.panel_activity.log("Barra Espaciadora: hablar con JARVIS | Tecla ESC: salir.")

    def _exit_system(self):
        QCoreApplication.quit()

    def _on_mic_clicked(self):
        if self.voice_engine:
            self.voice_engine.trigger_push_to_talk()

    def _on_user_request_state(self, new_state: SystemState):
        self.state_machine.transition_to(new_state, reason="Control manual")

    def _on_state_changed(self, new_state: SystemState, prev_state: SystemState):
        self.core_widget.set_state(new_state)
        self.lbl_status.setText(new_state.label)

    def keyPressEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return

        if event.key() == Qt.Key_Escape:
            self._exit_system()
        elif event.key() == Qt.Key_Space:
            self._on_mic_clicked()
            event.accept()
        else:
            key_map = {
                Qt.Key_1: SystemState.IDLE,
                Qt.Key_2: SystemState.LISTENING,
                Qt.Key_3: SystemState.THINKING,
                Qt.Key_4: SystemState.SPEAKING,
                Qt.Key_5: SystemState.EXECUTING,
                Qt.Key_6: SystemState.ERROR,
            }
            if event.key() in key_map:
                self._on_user_request_state(key_map[event.key()])
        super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), HologramTheme.BG_VOID)

        pen_grid = HologramTheme.GRID_LINE
        painter.setPen(pen_grid)
        w, h = self.width(), self.height()
        step = 40
        for x in range(0, w, step):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, step):
            painter.drawLine(0, y, w, y)