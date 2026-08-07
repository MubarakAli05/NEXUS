from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout

from src.ui.widgets.glass_card import GlassCard
from src.ui.theme.colors import Colors


class RecentProjects(GlassCard):

    def __init__(self):

        super().__init__("📂 Recent Projects")

        self.setMaximumHeight(220)

        projects = [
            "NEXUS AI",
            "FaceSecure",
            "Weather App",
            "Portfolio Website",
        ]

        for project in projects:

            item = QFrame()

            item.setStyleSheet("""
            QFrame{
                background:#162133;
                border:1px solid #22314A;
                border-radius:8px;
            }

            QFrame:hover{
                border:1px solid #22D3EE;
            }
            """)

            layout = QVBoxLayout(item)

            layout.setContentsMargins(12,8,12,8)

            label = QLabel(project)

            label.setStyleSheet(f"""
                color:{Colors.TEXT};
                font-size:14px;
                font-weight:500;
            """)

            layout.addWidget(label)

            self.content.addWidget(item)