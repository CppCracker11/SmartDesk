from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

BG = "#0D1212"
SURFACE = "#151C1C"
SURFACE_2 = "#1B2423"
ELEVATED = "#202B2A"
ACCENT = "#6FA7A3"
ACCENT_DARK = "#3F7775"
ACCENT_SOFT = "#284544"
TEXT = "#E8F0EF"
MUTED = "#91A3A1"
BORDER = "#30403F"
SUCCESS = "#7DBBAA"
DANGER = "#D98585"


def apply_theme(app) -> None:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(SURFACE))
    palette.setColor(QPalette.AlternateBase, QColor(SURFACE_2))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(SURFACE_2))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(ACCENT_DARK))
    palette.setColor(QPalette.HighlightedText, QColor(TEXT))
    app.setPalette(palette)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)


STYLESHEET = f"""
QMainWindow, QDialog {{
    background: {BG};
    color: {TEXT};
}}

QWidget {{
    font-family: "Segoe UI";
    font-size: 10.5pt;
    color: {TEXT};
}}

QFrame#card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 22px;
}}

QFrame#softCard {{
    background: {SURFACE_2};
    border: 1px solid rgba(111, 167, 163, 45);
    border-radius: 18px;
}}

QLabel#title {{
    font-size: 24pt;
    font-weight: 650;
    letter-spacing: 0.2px;
}}

QLabel#subtitle {{
    color: {MUTED};
    font-size: 10pt;
}}

QLabel#sectionLabel {{
    color: {MUTED};
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 1.5px;
}}

QLabel#pairCode {{
    font-size: 34pt;
    font-weight: 700;
    letter-spacing: 5px;
    color: {TEXT};
}}

QLabel#heroText {{
    font-size: 13pt;
    font-weight: 600;
}}

QLabel#muted {{
    color: {MUTED};
}}

QLabel#value {{
    color: {TEXT};
    font-weight: 600;
}}

QLabel#footer {{
    color: {MUTED};
    font-size: 9pt;
}}

QPushButton {{
    min-height: 38px;
    padding: 0 16px;
    border-radius: 13px;
    border: 1px solid {BORDER};
    background: {ELEVATED};
    color: {TEXT};
    font-weight: 600;
}}

QPushButton:hover {{
    background: #263331;
    border-color: {ACCENT_DARK};
}}

QPushButton:pressed {{
    background: #2B3B39;
}}

QPushButton#accent {{
    background: {ACCENT_DARK};
    border-color: {ACCENT_DARK};
}}

QPushButton#accent:hover {{
    background: #4B8784;
}}

QPushButton#danger {{
    color: {DANGER};
}}

QPushButton#flat {{
    background: transparent;
    border: 1px solid transparent;
    color: {MUTED};
}}

QPushButton#flat:hover {{
    background: {SURFACE_2};
    color: {TEXT};
}}

QLineEdit, QSpinBox {{
    min-height: 40px;
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 0 12px;
    selection-background-color: {ACCENT_DARK};
}}

QLineEdit:focus, QSpinBox:focus {{
    border-color: {ACCENT_DARK};
}}

QProgressBar {{
    min-height: 8px;
    max-height: 8px;
    border: none;
    border-radius: 4px;
    background: #25302F;
}}

QProgressBar::chunk {{
    border-radius: 4px;
    background: {ACCENT};
}}

QCheckBox {{
    spacing: 9px;
    color: {TEXT};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 6px;
    border: 1px solid {BORDER};
    background: {SURFACE_2};
}}

QCheckBox::indicator:checked {{
    background: {ACCENT_DARK};
    border-color: {ACCENT};
}}

QDialog QLabel#dialogTitle {{
    font-size: 18pt;
    font-weight: 650;
}}

QMenu {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    padding: 6px;
}}

QMenu::item {{
    padding: 8px 20px;
    border-radius: 8px;
}}

QMenu::item:selected {{
    background: {SURFACE_2};
}}
"""
