from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy,
    QStackedLayout,
)

from src.ui.widgets.top_bar import TopBar
from src.ui.widgets.voice_orb import VoiceOrb
from src.ui.widgets.background_animation import BackgroundAnimation
from src.ui.widgets.system_monitor import SystemMonitor
from src.ui.widgets.quick_actions import QuickActions
from src.ui.widgets.recent_projects import RecentProjects
from src.ui.widgets.today_panel import TodayPanel
from src.ui.widgets.command_bar import CommandBar

from src.ui.theme.colors import Colors


class DashboardLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        root = QVBoxLayout(self)

        root.setContentsMargins(30, 20, 30, 20)

        root.setSpacing(22)

        # =====================================================
        # TOP BAR
        # =====================================================

        self.topbar = TopBar()

        self.topbar.setFixedHeight(56)

        root.addWidget(self.topbar)

        # =====================================================
        # HERO SECTION
        # =====================================================

        hero = QWidget()

        hero.setFixedHeight(340)

        heroLayout = QVBoxLayout(hero)

        heroLayout.setContentsMargins(0, 0, 0, 0)

        heroLayout.setSpacing(10)

        heroLayout.setAlignment(Qt.AlignCenter)

        greeting = QLabel("Good Evening, Mubarak 👋")

        greeting.setAlignment(Qt.AlignCenter)

        greeting.setStyleSheet(f"""
            color:{Colors.TEXT};
            font-size:34px;
            font-weight:700;
        """)

        subtitle = QLabel("Ready to build something today?")

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet(f"""
            color:{Colors.TEXT_SECONDARY};
            font-size:16px;
        """)

        # -----------------------------------------------------
        # HERO CANVAS
        # -----------------------------------------------------

        heroCanvas = QWidget()

        heroCanvas.setFixedHeight(220)

        stack = QStackedLayout(heroCanvas)

        stack.setContentsMargins(0, 0, 0, 0)

        stack.setStackingMode(QStackedLayout.StackAll)

        background = BackgroundAnimation()
        background.setMinimumSize(0, 220)
        stack.addWidget(background)
        stack.setAlignment(background, Qt.AlignCenter)
        orb = VoiceOrb()

        stack.addWidget(background)

        stack.addWidget(orb)

        stack.setAlignment(
            orb,
            Qt.AlignCenter
        )

        # -----------------------------------------------------
        # HERO LAYOUT
        # -----------------------------------------------------

        heroLayout.addStretch()

        heroLayout.addWidget(greeting)

        heroLayout.addWidget(subtitle)

        heroLayout.addSpacing(10)

        heroLayout.addWidget(heroCanvas)

        heroLayout.addStretch()

        root.addWidget(hero)

        # =====================================================
        # CONTENT GRID
        # =====================================================

        grid = QGridLayout()

        grid.setContentsMargins(0, 0, 0, 0)

        grid.setHorizontalSpacing(20)

        grid.setVerticalSpacing(20)

        grid.setColumnStretch(0, 7)

        grid.setColumnStretch(1, 3)

        self.system = SystemMonitor()

        self.quick = QuickActions()

        self.projects = RecentProjects()

        self.today = TodayPanel()

        grid.addWidget(self.system, 0, 0)

        grid.addWidget(self.quick, 0, 1)

        grid.addWidget(self.projects, 1, 0)

        grid.addWidget(self.today, 1, 1)

        root.addLayout(grid, 1)

        # =====================================================
        # COMMAND BAR
        # =====================================================

        self.command = CommandBar()

        self.command.setFixedHeight(58)

        root.addWidget(self.command)