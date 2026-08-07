from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QStackedWidget,
)

from src.ui.widgets.sidebar import Sidebar

from src.ui.dashboard.layout import DashboardLayout
from src.ui.chat.page import ChatPage


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("Dashboard")

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        main = QHBoxLayout(self)

        main.setContentsMargins(0, 0, 0, 0)

        main.setSpacing(0)

        # ==========================================
        # Sidebar
        # ==========================================

        self.sidebar = Sidebar()

        self.sidebar.setFixedWidth(240)

        main.addWidget(self.sidebar)

        # ==========================================
        # Pages
        # ==========================================

        self.pages = QStackedWidget()

        self.pages.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # Page 0

        self.dashboardPage = DashboardLayout()

        self.pages.addWidget(self.dashboardPage)

        # Page 1

        self.chatPage = ChatPage()

        self.pages.addWidget(self.chatPage)

        main.addWidget(self.pages, 1)

        # ==========================================
        # Temporary
        # ==========================================

        # Opens Chat immediately so we can develop it

        self.pages.setCurrentIndex(1)