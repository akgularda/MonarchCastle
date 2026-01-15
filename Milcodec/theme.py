"""
MILCODEC DESIGN SYSTEM v2.0
===========================
Professional, military-grade UI theming inspired by Palantir Gotham.
Provides consistent styling across all Milcodec applications.
"""

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QFontDatabase, QColor, QLinearGradient, QPalette
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
import os

# =============================================================================
# COLOR PALETTE
# =============================================================================
class Colors:
    """Palantir-inspired dark theme color palette."""
    
    # Core Background Layers
    VOID = "#0a0a0f"           # Deepest background
    BACKGROUND = "#0d0d14"     # Primary background
    SURFACE = "#14141f"        # Card/panel background
    ELEVATED = "#1a1a2e"       # Elevated elements
    
    # Borders & Dividers
    BORDER_DIM = "#1e1e2e"     # Subtle borders
    BORDER = "#2a2a3e"         # Standard borders
    BORDER_ACCENT = "#3a3a5e"  # Highlighted borders
    
    # Text Hierarchy
    TEXT_PRIMARY = "#e8e8f0"   # Primary text
    TEXT_SECONDARY = "#a0a0b8" # Secondary text
    TEXT_DIM = "#606078"       # Disabled/dim text
    
    # Accent Colors - Tactical
    CYAN = "#00d4ff"           # Primary accent (secure/info)
    CYAN_DIM = "#0088aa"       # Dimmed cyan
    AMBER = "#ffb000"          # Warning/command accent
    AMBER_DIM = "#aa7500"      # Dimmed amber
    GREEN = "#00ff88"          # Success/active
    GREEN_DIM = "#00aa55"      # Dimmed green
    RED = "#ff3355"            # Alert/danger
    RED_DIM = "#aa2233"        # Dimmed red
    
    # Special Effects
    GLOW_CYAN = "rgba(0, 212, 255, 0.3)"
    GLOW_AMBER = "rgba(255, 176, 0, 0.3)"
    GLOW_GREEN = "rgba(0, 255, 136, 0.3)"
    GLOW_RED = "rgba(255, 51, 85, 0.3)"
    
    # Gradients (CSS format)
    GRADIENT_HEADER = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a2e, stop:1 #14141f)"
    GRADIENT_PANEL = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #14141f, stop:1 #0d0d14)"
    GRADIENT_BUTTON = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a2a3e, stop:1 #1a1a2e)"

# =============================================================================
# TYPOGRAPHY
# =============================================================================
class Fonts:
    """Font configuration with Inter as primary, JetBrains Mono for code."""
    
    # Font family names
    PRIMARY = "Inter"
    MONO = "JetBrains Mono"
    FALLBACK = "Segoe UI"
    MONO_FALLBACK = "Consolas"
    
    # Font sizes
    SIZE_TINY = 9
    SIZE_SMALL = 10
    SIZE_BODY = 11
    SIZE_LARGE = 13
    SIZE_TITLE = 16
    SIZE_HEADER = 20
    SIZE_DISPLAY = 28
    
    @staticmethod
    def get_font(size=11, bold=False, mono=False):
        """Get a configured QFont with proper fallbacks."""
        family = Fonts.MONO if mono else Fonts.PRIMARY
        fallback = Fonts.MONO_FALLBACK if mono else Fonts.FALLBACK
        
        font = QFont(family, size)
        if not font.exactMatch():
            font = QFont(fallback, size)
        
        if bold:
            font.setWeight(QFont.Weight.DemiBold)
        
        return font

# =============================================================================
# STYLESHEET COMPONENTS
# =============================================================================
class Styles:
    """Reusable stylesheet strings for Qt widgets."""
    
    @staticmethod
    def main_window():
        return f"""
            QMainWindow {{
                background-color: {Colors.BACKGROUND};
            }}
        """
    
    @staticmethod
    def sidebar():
        return f"""
            QFrame#Sidebar {{
                background-color: {Colors.SURFACE};
                border-right: 1px solid {Colors.BORDER_DIM};
            }}
            QFrame#Sidebar QPushButton {{
                background: transparent;
                border: none;
                color: {Colors.TEXT_SECONDARY};
                text-align: left;
                padding: 12px 16px;
                font-size: 11pt;
            }}
            QFrame#Sidebar QPushButton:hover {{
                background-color: {Colors.ELEVATED};
                color: {Colors.TEXT_PRIMARY};
            }}
            QFrame#Sidebar QPushButton:checked {{
                background-color: {Colors.ELEVATED};
                color: {Colors.CYAN};
                border-left: 3px solid {Colors.CYAN};
            }}
        """
    
    @staticmethod
    def header():
        return f"""
            QFrame#Header {{
                background: {Colors.GRADIENT_HEADER};
                border-bottom: 1px solid {Colors.BORDER};
                padding: 8px 16px;
            }}
            QFrame#Header QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
            QFrame#Header QLabel#Title {{
                font-size: 14pt;
                font-weight: 600;
                color: {Colors.CYAN};
            }}
            QFrame#Header QLabel#Subtitle {{
                font-size: 10pt;
                color: {Colors.TEXT_SECONDARY};
            }}
        """
    
    @staticmethod
    def panel():
        return f"""
            QFrame.Panel {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
            }}
            QFrame.Panel QLabel.PanelTitle {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 9pt;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """
    
    @staticmethod
    def text_input():
        return f"""
            QLineEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-family: '{Fonts.MONO}', '{Fonts.MONO_FALLBACK}';
                font-size: 11pt;
                selection-background-color: {Colors.CYAN_DIM};
            }}
            QLineEdit:focus {{
                border-color: {Colors.CYAN};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_DIM};
            }}
        """
    
    @staticmethod
    def text_area():
        return f"""
            QTextEdit {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                font-family: '{Fonts.MONO}', '{Fonts.MONO_FALLBACK}';
                font-size: 10pt;
                selection-background-color: {Colors.CYAN_DIM};
            }}
            QTextEdit:focus {{
                border-color: {Colors.CYAN};
            }}
        """
    
    @staticmethod
    def button_primary():
        return f"""
            QPushButton {{
                background: {Colors.GRADIENT_BUTTON};
                border: 1px solid {Colors.CYAN_DIM};
                border-radius: 4px;
                padding: 10px 20px;
                color: {Colors.CYAN};
                font-weight: 600;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {Colors.CYAN_DIM};
                border-color: {Colors.CYAN};
            }}
            QPushButton:pressed {{
                background-color: {Colors.CYAN};
                color: {Colors.VOID};
            }}
            QPushButton:disabled {{
                background-color: {Colors.SURFACE};
                border-color: {Colors.BORDER_DIM};
                color: {Colors.TEXT_DIM};
            }}
        """
    
    @staticmethod
    def button_danger():
        return f"""
            QPushButton {{
                background: {Colors.GRADIENT_BUTTON};
                border: 1px solid {Colors.RED_DIM};
                border-radius: 4px;
                padding: 10px 20px;
                color: {Colors.RED};
                font-weight: 600;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {Colors.RED_DIM};
                border-color: {Colors.RED};
            }}
            QPushButton:pressed {{
                background-color: {Colors.RED};
                color: {Colors.VOID};
            }}
        """
    
    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px 16px;
                color: {Colors.TEXT_SECONDARY};
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {Colors.ELEVATED};
                border-color: {Colors.BORDER_ACCENT};
                color: {Colors.TEXT_PRIMARY};
            }}
        """
    
    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
                padding: 4px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 10pt;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 3px;
            }}
            QListWidget::item:hover {{
                background-color: {Colors.ELEVATED};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.CYAN_DIM};
                color: {Colors.TEXT_PRIMARY};
            }}
        """
    
    @staticmethod
    def progress_bar():
        return f"""
            QProgressBar {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 3px;
                height: 8px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.CYAN_DIM}, stop:1 {Colors.CYAN});
                border-radius: 2px;
            }}
        """
    
    @staticmethod
    def scrollbar():
        return f"""
            QScrollBar:vertical {{
                background: {Colors.SURFACE};
                width: 10px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {Colors.BORDER_ACCENT};
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Colors.CYAN_DIM};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar:horizontal {{
                background: {Colors.SURFACE};
                height: 10px;
                margin: 0;
            }}
            QScrollBar::handle:horizontal {{
                background: {Colors.BORDER_ACCENT};
                min-width: 30px;
                border-radius: 5px;
            }}
        """
    
    @staticmethod
    def tooltip():
        return f"""
            QToolTip {{
                background-color: {Colors.ELEVATED};
                border: 1px solid {Colors.BORDER};
                color: {Colors.TEXT_PRIMARY};
                padding: 6px;
                font-size: 10pt;
            }}
        """
    
    @staticmethod
    def tab_widget():
        return f"""
            QTabWidget::pane {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {Colors.BACKGROUND};
                border: 1px solid {Colors.BORDER_DIM};
                border-bottom: none;
                padding: 8px 16px;
                margin-right: 2px;
                color: {Colors.TEXT_SECONDARY};
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.SURFACE};
                color: {Colors.CYAN};
                border-color: {Colors.CYAN_DIM};
            }}
            QTabBar::tab:hover {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """
    
    @staticmethod
    def combo_box():
        return f"""
            QComboBox {{
                background-color: {Colors.VOID};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 10pt;
            }}
            QComboBox:hover {{
                border-color: {Colors.CYAN_DIM};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.CYAN_DIM};
            }}
        """
    
    @staticmethod
    def group_box():
        return f"""
            QGroupBox {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER_DIM};
                border-radius: 6px;
                margin-top: 16px;
                padding: 16px;
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: {Colors.TEXT_SECONDARY};
                font-size: 9pt;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def apply_theme(app: QApplication):
    """Apply the Milcodec theme to the entire application."""
    # Set application-wide palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(Colors.BACKGROUND))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Colors.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(Colors.VOID))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Colors.SURFACE))
    palette.setColor(QPalette.ColorRole.Text, QColor(Colors.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(Colors.SURFACE))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Colors.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Colors.CYAN_DIM))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Colors.TEXT_PRIMARY))
    app.setPalette(palette)
    
    # Set default font
    app.setFont(Fonts.get_font(Fonts.SIZE_BODY))
    
    # Apply global stylesheet
    app.setStyleSheet(
        Styles.scrollbar() + 
        Styles.tooltip()
    )

def create_glow_effect(widget: QWidget, color: str = Colors.CYAN, blur: int = 15):
    """Add a subtle glow effect to a widget."""
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setColor(QColor(color))
    effect.setOffset(0, 0)
    widget.setGraphicsEffect(effect)

def animate_fade_in(widget: QWidget, duration: int = 300):
    """Create a fade-in animation for a widget."""
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    return animation

# =============================================================================
# STATUS INDICATORS
# =============================================================================
class StatusColors:
    """Status-specific color mappings."""
    
    SECURE = Colors.GREEN
    CONNECTED = Colors.CYAN
    PENDING = Colors.AMBER
    WARNING = Colors.AMBER
    ERROR = Colors.RED
    OFFLINE = Colors.TEXT_DIM
    
    @staticmethod
    def get_status_style(status: str):
        """Get stylesheet for status indicator dot."""
        color_map = {
            'SECURE': StatusColors.SECURE,
            'CONNECTED': StatusColors.CONNECTED,
            'PENDING': StatusColors.PENDING,
            'WARNING': StatusColors.WARNING,
            'ERROR': StatusColors.ERROR,
            'OFFLINE': StatusColors.OFFLINE,
        }
        color = color_map.get(status.upper(), StatusColors.OFFLINE)
        return f"""
            QLabel {{
                background-color: {color};
                border-radius: 4px;
                min-width: 8px;
                max-width: 8px;
                min-height: 8px;
                max-height: 8px;
            }}
        """

# =============================================================================
# CLASSIFICATION BANNERS
# =============================================================================
class Classification:
    """Classification level styling."""
    
    @staticmethod
    def banner(level: str = "UNCLASSIFIED"):
        """Get stylesheet for classification banner."""
        colors = {
            "UNCLASSIFIED": (Colors.GREEN, Colors.VOID),
            "CONFIDENTIAL": (Colors.CYAN, Colors.VOID),
            "SECRET": (Colors.RED, Colors.TEXT_PRIMARY),
            "TOP SECRET": ("#ff8800", Colors.VOID),
        }
        bg, fg = colors.get(level.upper(), (Colors.GREEN, Colors.VOID))
        return f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                font-size: 8pt;
                font-weight: bold;
                padding: 2px 8px;
                letter-spacing: 2px;
            }}
        """

# =============================================================================
# COMPOSITE GLOBAL STYLESHEET
# =============================================================================
def get_complete_stylesheet():
    """Get the complete application stylesheet."""
    return (
        Styles.main_window() +
        Styles.sidebar() +
        Styles.header() +
        Styles.panel() +
        Styles.text_input() +
        Styles.text_area() +
        Styles.button_primary() +
        Styles.list_widget() +
        Styles.progress_bar() +
        Styles.scrollbar() +
        Styles.tooltip() +
        Styles.tab_widget() +
        Styles.combo_box() +
        Styles.group_box()
    )
