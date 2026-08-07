from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)

from PySide6.QtCore import Qt

from src.ui.widgets.search_bar import SearchBar
from src.ui.theme.colors import Colors
from src.ui.theme.radius import Radius
from src.ui.theme.spacing import Spacing


class TopBar(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(Spacing.MD)

        # ------------------------
        # Search
        # ------------------------

        self.search = SearchBar()

        self.search.setMinimumHeight(52)

        layout.addWidget(self.search, 1)

        # ------------------------
        # Right Buttons
        # ------------------------

        icons = [
            "🔔",
            "⚙",
            "👤"
        ]

        for icon in icons:

            button = QPushButton(icon)

            button.setCursor(Qt.PointingHandCursor)

            button.setFixedSize(50, 50)

            button.setStyleSheet(f"""
            QPushButton{{
                background:{Colors.PANEL};

                color:white;

                border:1px solid {Colors.BORDER};

                border-radius:{Radius.BUTTON}px;

                font-size:18px;
            }}

            QPushButton:hover{{
                background:{Colors.PANEL_LIGHT};

                border:1px solid {Colors.PRIMARY};
            }}

            QPushButton:pressed{{
                background:#101826;
            }}
            """)

            layout.addWidget(button)