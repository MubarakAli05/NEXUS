from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from src.ui.theme.colors import Colors
from src.ui.theme.radius import Radius


class SearchBar(QLineEdit):

    def __init__(self):

        super().__init__()

        self.setPlaceholderText("🔍  Search anything or ask NEXUS...")

        self.setMinimumHeight(52)

        self.setClearButtonEnabled(True)

        self.setAlignment(Qt.AlignVCenter)

        self.setStyleSheet(f"""
        QLineEdit{{
            background:{Colors.SEARCH};

            color:{Colors.TEXT};

            border:1px solid {Colors.BORDER};

            border-radius:{Radius.SEARCH}px;

            padding-left:18px;

            padding-right:18px;

            font-size:15px;

            selection-background-color:{Colors.PRIMARY};
        }}

        QLineEdit:focus{{
            border:1px solid {Colors.PRIMARY};

            background:#111C2B;
        }}

        QLineEdit::placeholder{{
            color:{Colors.TEXT_SECONDARY};
        }}
        """)