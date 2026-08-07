from PySide6.QtWidgets import QPushButton

from src.ui.theme.colors import Colors
from src.ui.theme.radius import Radius


class GlowButton(QPushButton):

    def __init__(self, text="", icon=""):

        super().__init__()

        self.setText(f"{icon}  {text}")

        self.setMinimumHeight(54)

        self.setStyleSheet(f"""
        QPushButton{{
            background:{Colors.PANEL_LIGHT};
            color:white;
            border:1px solid {Colors.BORDER};
            border-radius:{Radius.BUTTON}px;
            font-size:15px;
            text-align:left;
            padding-left:18px;
        }}

        QPushButton:hover{{
            border:1px solid {Colors.PRIMARY};
            background:#1C2940;
        }}
        """)