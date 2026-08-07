from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
)

from src.ui.chat.chat_sidebar import ChatSidebar
from src.ui.chat.chat_area import ChatArea


class ChatPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("ChatPage")

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.setStyleSheet("""
        QWidget#ChatPage{
            background:#090E17;
        }
        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        # ----------------------------------
        # Conversation Sidebar
        # ----------------------------------

        self.sidebar = ChatSidebar()

        self.sidebar.setFixedWidth(320)

        layout.addWidget(self.sidebar)

        # ----------------------------------
        # Main Chat Area
        # ----------------------------------

        self.chatArea = ChatArea()

        layout.addWidget(
            self.chatArea,
            1
        )