from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from src.ui.theme.colors import Colors
from src.ui.theme.radius import Radius


class SidebarButton(QPushButton):

    def __init__(self, text, icon="", active=False):

        super().__init__(f"{icon}   {text}")

        self.setCursor(Qt.PointingHandCursor)

        self.setMinimumHeight(52)
        self.setMaximumHeight(52)

        if active:

            self.setStyleSheet(f"""
            QPushButton{{
                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:0,
                    stop:0 #13304A,
                    stop:1 #0F1D2F
                );

                color:white;

                border:1px solid {Colors.PRIMARY};

                border-radius:{Radius.BUTTON}px;

                padding-left:18px;

                text-align:left;

                font-size:16px;

                font-weight:600;
            }}

            QPushButton:hover{{
                background:#183652;
            }}
            """)

        else:

            self.setStyleSheet(f"""
            QPushButton{{
                background:transparent;

                color:#CBD5E1;

                border:none;

                border-radius:{Radius.BUTTON}px;

                padding-left:18px;

                text-align:left;

                font-size:15px;

                font-weight:500;
            }}

            QPushButton:hover{{
                background:#111827;

                color:white;

                padding-left:24px;
            }}

            QPushButton:pressed{{
                background:#162133;
            }}
            """)