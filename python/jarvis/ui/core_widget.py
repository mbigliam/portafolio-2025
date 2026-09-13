"""
Núcleo Visual Reactivo e Interactivo de JARVIS (Holographic Reactor Core).
Renderizado de precisión a 60 FPS con QPainter.
"""
import math
import random
from typing import List
from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget

from core.state import SystemState
from ui.themes import HologramTheme


class Particle:
    """Partícula de energía que orbita alrededor del reactor."""

    def __init__(self, base_radius: float):
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.01, 0.035) * random.choice([-1, 1])
        self.distance = base_radius + random.uniform(-40, 60)
        self.size = random.uniform(1.5, 3.5)
        self.opacity = random.uniform(0.3, 0.9)

    def update(self, speed_mult: float, target_radius: float):
        self.angle += self.speed * speed_mult
        self.distance += (target_radius - self.distance) * 0.05


class HolographicCoreWidget(QWidget):
    """Widget que dibuja el núcleo animado tipo Reactor Ark."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = SystemState.STARTING

        # Variables de Animación Continua
        self.angle_ring1 = 0.0
        self.angle_ring2 = 0.0
        self.angle_ring3 = 0.0
        self.pulse_phase = 0.0
        self.wave_phase = 0.0

        # Partículas
        self.particles: List[Particle] = [Particle(150.0) for _ in range(70)]

        # Timer de renderizado continuo (60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate_step)
        self.timer.start(16)

    def set_state(self, new_state: SystemState) -> None:
        self.state = new_state
        self.update()

    def _animate_step(self) -> None:
        # Velocidades y modulaciones reactivas según el estado
        if self.state == SystemState.THINKING:
            speed = 3.5
            pulse_speed = 0.12
        elif self.state == SystemState.SPEAKING:
            speed = 2.0
            pulse_speed = 0.15
        elif self.state == SystemState.LISTENING:
            speed = 1.2
            pulse_speed = 0.08
        elif self.state == SystemState.EXECUTING:
            speed = 2.8
            pulse_speed = 0.10
        elif self.state == SystemState.ERROR:
            speed = 0.5
            pulse_speed = 0.20
        else:  # IDLE o STARTING
            speed = 1.0
            pulse_speed = 0.04

        self.angle_ring1 = (self.angle_ring1 + 0.8 * speed) % 360
        self.angle_ring2 = (self.angle_ring2 - 1.2 * speed) % 360
        self.angle_ring3 = (self.angle_ring3 + 1.8 * speed) % 360
        self.pulse_phase = (self.pulse_phase + pulse_speed) % (2 * math.pi)
        self.wave_phase = (self.wave_phase + 0.15 * speed) % (2 * math.pi)

        # Actualizar partículas
        for p in self.particles:
            p.update(speed, 140.0 + (math.sin(self.pulse_phase) * 15))

        self.update()

    def _get_state_colors(self):
        mapping = {
            SystemState.IDLE: (HologramTheme.CORE_IDLE, HologramTheme.CORE_IDLE_GLOW),
            SystemState.LISTENING: (HologramTheme.CORE_LISTENING, HologramTheme.CORE_LISTENING_GLOW),
            SystemState.THINKING: (HologramTheme.CORE_THINKING, HologramTheme.CORE_THINKING_GLOW),
            SystemState.SPEAKING: (HologramTheme.CORE_SPEAKING, HologramTheme.CORE_SPEAKING_GLOW),
            SystemState.EXECUTING: (HologramTheme.CORE_EXECUTING, HologramTheme.CORE_EXECUTING_GLOW),
            SystemState.ERROR: (HologramTheme.CORE_ERROR, HologramTheme.CORE_ERROR_GLOW),
            SystemState.STARTING: (HologramTheme.CORE_IDLE, HologramTheme.CORE_IDLE_GLOW),
            SystemState.OFFLINE: (QColor(100, 100, 100), QColor(60, 60, 60, 80)),
        }
        return mapping.get(self.state, (HologramTheme.CORE_IDLE, HologramTheme.CORE_IDLE_GLOW))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w, h = self.width(), self.height()
        center_x, center_y = w / 2.0, h / 2.0
        base_color, glow_color = self._get_state_colors()

        # 1. Fondo de energía difusa (Aura Central)
        pulse = (math.sin(self.pulse_phase) + 1.0) / 2.0  # Rango 0.0 a 1.0
        glow_radius = 180 + (pulse * 35)

        gradient = QRadialGradient(QPointF(center_x, center_y), glow_radius)
        gradient.setColorAt(0.0, glow_color)
        gradient.setColorAt(0.6, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 25))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, w, h, QBrush(gradient))

        # 2. Dibujar Partículas Flotantes
        for p in self.particles:
            px = center_x + math.cos(p.angle) * p.distance
            py = center_y + math.sin(p.angle) * p.distance
            part_col = QColor(base_color)
            part_col.setAlphaF(p.opacity)
            painter.setPen(Qt.NoPen)
            painter.setBrush(part_col)
            painter.drawEllipse(QPointF(px, py), p.size, p.size)

        # 3. Anillo Exterior con Muescas y Segmentos
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle_ring1)

        pen_ring1 = QPen(QColor(base_color.red(), base_color.green(), base_color.blue(), 120), 1.5)
        pen_ring1.setStyle(Qt.DashLine)
        pen_ring1.setDashPattern([15, 8, 2, 8])
        painter.setPen(pen_ring1)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRectF(-150, -150, 300, 300))

        # 4. Muescas Cardinales
        pen_ticks = QPen(base_color, 2)
        painter.setPen(pen_ticks)
        for i in range(12):
            angle = i * (360 / 12)
            rad = math.radians(angle)
            x1 = math.cos(rad) * 155
            y1 = math.sin(rad) * 155
            x2 = math.cos(rad) * 165
            y2 = math.sin(rad) * 165
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        painter.restore()

        # 5. Anillo Intermedio Contrarrotatorio con Arcos de Energía
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle_ring2)

        pen_arc = QPen(base_color, 3.0)
        painter.setPen(pen_arc)
        painter.drawArc(QRectF(-120, -120, 240, 240), 0 * 16, 70 * 16)
        painter.drawArc(QRectF(-120, -120, 240, 240), 120 * 16, 70 * 16)
        painter.drawArc(QRectF(-120, -120, 240, 240), 240 * 16, 70 * 16)
        painter.restore()

        # 6. Ondas de Audio / Espectro Reactivo (Modo LISTENING y SPEAKING)
        if self.state in (SystemState.LISTENING, SystemState.SPEAKING):
            painter.save()
            painter.translate(center_x, center_y)
            path = QPainterPath()
            wave_points = 64
            for i in range(wave_points + 1):
                ang = i * (2 * math.pi / wave_points)
                amp = math.sin(ang * 6 + self.wave_phase) * (18 * pulse + 5)
                r = 85 + amp
                x = math.cos(ang) * r
                y = math.sin(ang) * r
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            pen_wave = QPen(QColor(base_color.red(), base_color.green(), base_color.blue(), 180), 2.0)
            painter.setPen(pen_wave)
            painter.drawPath(path)
            painter.restore()

        # 7. Núcleo Interno Sólido con Gradiente de Luz
        core_r = 55 + (pulse * 8)
        core_grad = QRadialGradient(QPointF(center_x, center_y), core_r)
        core_grad.setColorAt(0.0, QColor(255, 255, 255, 240))
        core_grad.setColorAt(0.4, base_color)
        core_grad.setColorAt(1.0, QColor(base_color.red(), base_color.green(), base_color.blue(), 40))

        painter.setPen(QPen(base_color, 2))
        painter.setBrush(QBrush(core_grad))
        painter.drawEllipse(QPointF(center_x, center_y), core_r, core_r)

        # 8. Texto de Identificación y Estado en el Centro
        painter.setFont(QFont(HologramTheme.FONT_FAMILY, 11, QFont.Bold))
        painter.setPen(QColor("#ffffff"))
        text = "J.A.R.V.I.S."
        fm = painter.fontMetrics()
        painter.drawText(int(center_x - fm.horizontalAdvance(text) / 2), int(center_y - 4), text)

        painter.setFont(QFont(HologramTheme.FONT_MONO, 7, QFont.Bold))
        painter.setPen(QColor(HologramTheme.TEXT_SECONDARY))
        status_code = f"CORE: {self.state.name}"
        fm_s = painter.fontMetrics()
        painter.drawText(int(center_x - fm_s.horizontalAdvance(status_code) / 2), int(center_y + 14), status_code)