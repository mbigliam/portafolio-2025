"""
Constantes de Diseño, Paleta Futurista e Identidad Visual para JARVIS.
"""
from PySide6.QtGui import QColor


class HologramTheme:
    # Fondos oscuros de cristal futurista
    BG_VOID = QColor(6, 10, 18, 245)
    PANEL_BG = QColor(10, 20, 36, 160)
    PANEL_BORDER = QColor(0, 229, 255, 60)
    GRID_LINE = QColor(0, 180, 255, 20)

    # Colores Reactivos del Núcleo según Estado
    CORE_IDLE = QColor(0, 229, 255)       # Cian Eléctrico
    CORE_IDLE_GLOW = QColor(0, 140, 255, 80)

    CORE_LISTENING = QColor(0, 255, 170)  # Esmeralda Turquesa Neón
    CORE_LISTENING_GLOW = QColor(0, 255, 150, 100)

    CORE_THINKING = QColor(255, 170, 0)   # Ámbar Dorado Reactor
    CORE_THINKING_GLOW = QColor(255, 140, 0, 100)

    CORE_SPEAKING = QColor(130, 240, 255) # Blanco Azulado Intenso
    CORE_SPEAKING_GLOW = QColor(0, 200, 255, 140)

    CORE_EXECUTING = QColor(190, 0, 255)  # Magenta / Púrpura Alta Energía
    CORE_EXECUTING_GLOW = QColor(150, 0, 255, 100)

    CORE_ERROR = QColor(255, 30, 70)      # Carmesí de Advertencia
    CORE_ERROR_GLOW = QColor(255, 0, 50, 120)

    # Tipografía y Textos
    TEXT_PRIMARY = "#e6f7ff"
    TEXT_SECONDARY = "#6bb3d9"
    TEXT_ACCENT = "#00e5ff"
    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"