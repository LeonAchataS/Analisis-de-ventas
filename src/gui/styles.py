"""
Estilos y configuración de colores para la GUI.
"""

# Colores principales
PRIMARY_COLOR = "#2E86AB"
SECONDARY_COLOR = "#A23B72"
SUCCESS_COLOR = "#06A77D"
WARNING_COLOR = "#F18F01"
DANGER_COLOR = "#C73E1D"
BG_COLOR = "#F7F9FB"
TEXT_COLOR = "#2D3748"
LIGHT_GRAY = "#E2E8F0"
DARK_GRAY = "#4A5568"

# Fuentes
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 18
FONT_SIZE_SUBTITLE = 14
FONT_SIZE_NORMAL = 11
FONT_SIZE_SMALL = 9

# Configuración de estilo para ttk widgets
TTK_STYLE_CONFIG = {
    "TButton": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            "borderwidth": 0,
            "focuscolor": "none",
        }
    },
    "Primary.TButton": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            "background": PRIMARY_COLOR,
            "foreground": "white",
            "borderwidth": 0,
        }
    },
    "TLabel": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_NORMAL),
            "background": BG_COLOR,
        }
    },
    "Title.TLabel": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            "foreground": PRIMARY_COLOR,
            "background": BG_COLOR,
        }
    },
    "Subtitle.TLabel": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_SUBTITLE),
            "foreground": TEXT_COLOR,
            "background": BG_COLOR,
        }
    },
    "TFrame": {
        "configure": {
            "background": BG_COLOR,
        }
    },
}

# Dimensiones
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
PADDING = 20
BUTTON_HEIGHT = 40
