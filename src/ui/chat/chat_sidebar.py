from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)


class ChatSidebar(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("ChatSidebar")

        self.setStyleSheet("""
        QWidget#ChatSidebar{
            background:#0D1117;
            border-right:1px solid #1F2937;
        }

        QLabel{
            color:white;
        }

        QLineEdit{
            background:#111827;
            border:1px solid #243247;
            border-radius:10px;
            color:white;
            padding:10px;
            font-size:14px;
        }

        QLineEdit:focus{
            border:1px solid #22D3EE;
        }

        QPushButton{
            background:#22D3EE;
            color:black;
            border:none;
            border-radius:10px;
            font-size:14px;
            font-weight:600;
            padding:12px;
        }

        QPushButton:hover{
            background:#38BDF8;
        }

        QListWidget{
            background:transparent;
            border:none;
            color:white;
            outline:none;
            font-size:14px;
        }

        QListWidget::item{
            padding:12px;
            border-radius:8px;
            margin-bottom:4px;
        }

        QListWidget::item:selected{
            background:#1E293B;
        }

        QListWidget::item:hover{
            background:#162133;
        }
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(15)

        # ----------------------------------
        # Title
        # ----------------------------------

        title = QLabel("NEXUS Chat")

        title.setAlignment(Qt.AlignLeft)

        title.setStyleSheet("""
            font-size:24px;
            font-weight:700;
            color:white;
        """)

        layout.addWidget(title)

        # ----------------------------------
        # New Chat
        # ----------------------------------

        self.newChat = QPushButton("+ New Chat")

        self.newChat.setFixedHeight(45)

        layout.addWidget(self.newChat)

        # ----------------------------------
        # Search
        # ----------------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText("Search conversations...")

        self.search.setFixedHeight(42)

        layout.addWidget(self.search)

        # ----------------------------------
        # Conversation List
        # ----------------------------------

        self.history = QListWidget()

        chats = [
            "💬 Welcome to NEXUS",
            "🐍 Python Assistant",
            "💻 FaceSecure",
            "🌦 Weather Project",
            "📁 Portfolio",
            "⚙ Automation",
            "🧠 Memory Test",
            "🎤 Voice Assistant",
        ]

        for chat in chats:

            item = QListWidgetItem(chat)

            self.history.addItem(item)

        layout.addWidget(self.history)

        # ----------------------------------
        # Bottom Profile
        # ----------------------------------

        profile = QLabel("👤 Mubarak\nNEXUS Premium")

        profile.setStyleSheet("""
            background:#111827;
            border:1px solid #243247;
            border-radius:12px;
            padding:12px;
            font-size:13px;
        """)

        layout.addWidget(profile)