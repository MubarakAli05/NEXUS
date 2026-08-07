from PySide6.QtWidgets import QLabel

from src.ui.theme.colors import Colors


class StatusChip(QLabel):

    def __init__(self):

        super().__init__("🟢  NEXUS Online")

        self.setFixedHeight(42)

        self.setStyleSheet(f"""
        QLabel{{
            background:#10311F;
            color:{Colors.SUCCESS};
            border-radius:12px;
            padding-left:18px;
            font-size:14px;
            font-weight:600;
        }}
        """)