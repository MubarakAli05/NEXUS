from datetime import datetime

from PySide6.QtWidgets import QLabel

from src.ui.widgets.glass_card import GlassCard
from src.ui.theme.colors import Colors


class TodayPanel(GlassCard):

    def __init__(self):

        super().__init__("📅 Today")

        self.setMaximumHeight(220)

        today = datetime.now()

        day = QLabel(today.strftime("%A"))

        date = QLabel(today.strftime("%d %B %Y"))

        weather = QLabel("☀ 28°C")

        day.setStyleSheet(f"""
            color:{Colors.TEXT};
            font-size:20px;
            font-weight:600;
        """)

        date.setStyleSheet(f"""
            color:#94A3B8;
            font-size:15px;
        """)

        weather.setStyleSheet(f"""
            color:{Colors.PRIMARY};
            font-size:26px;
            font-weight:bold;
        """)

        self.content.addWidget(day)

        self.content.addWidget(date)

        self.content.addSpacing(8)

        self.content.addWidget(weather)