from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QTimer,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
)

from src.core.ai.ai_engine import AIEngine

from src.ui.chat.message_bubble import MessageBubble
from src.ui.chat.typing_indicator import TypingIndicator
from src.ui.chat.input_bar import InputBar


# ==========================================================
# AI WORKER
# ==========================================================

class AIWorker(QThread):

    finished = Signal(str)

    def __init__(self, ai, message):

        super().__init__()

        self.ai = ai
        self.message = message

    def run(self):

        reply = self.ai.ask(self.message)

        self.finished.emit(reply)


# ==========================================================
# CHAT AREA
# ==========================================================

class ChatArea(QWidget):

    def __init__(self):

        super().__init__()

        self.ai = AIEngine()

        self.setObjectName("ChatArea")

        self.setStyleSheet("""
        QWidget#ChatArea{
            background:#090E17;
        }

        QLabel{
            color:white;
        }

        QScrollArea{
            border:none;
            background:transparent;
        }

        QScrollBar:vertical{
            width:10px;
            background:#090E17;
            border:none;
        }

        QScrollBar::handle:vertical{
            background:#243247;
            border-radius:5px;
        }

        QScrollBar::handle:vertical:hover{
            background:#22D3EE;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical{
            height:0px;
        }
        """)

        # ==================================================
        # MAIN LAYOUT
        # ==================================================

        self.main = QVBoxLayout(self)

        self.main.setContentsMargins(24, 20, 24, 20)

        self.main.setSpacing(18)

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        title = QLabel("💬 NEXUS Assistant")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:700;
            color:white;
        """)

        status = QLabel("🟢 Online")

        status.setStyleSheet("""
            color:#22C55E;
            font-size:14px;
            font-weight:600;
        """)

        header.addWidget(title)

        header.addStretch()

        header.addWidget(status)

        self.main.addLayout(header)

        # ==================================================
        # CHAT SCROLL AREA
        # ==================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()

        self.messages = QVBoxLayout(container)

        self.messages.setAlignment(Qt.AlignTop)

        self.messages.setSpacing(14)

        self.messages.setContentsMargins(
            0,
            10,
            0,
            10,
        )
                # ==================================================
        # WELCOME MESSAGE
        # ==================================================

        self.add_message(
            "Hello Mubarak 👋\n\n"
            "I'm NEXUS.\n\n"
            "Your personal AI assistant.\n"
            "How can I help you today?",
            "assistant"
        )

        self.scroll.setWidget(container)

        self.main.addWidget(self.scroll, 1)

        # ==================================================
        # INPUT BAR
        # ==================================================

        self.inputBar = InputBar()

        self.main.addWidget(self.inputBar)

        # ==================================================
        # SIGNALS
        # ==================================================

        self.inputBar.send.clicked.connect(
            self.send_message
        )

        self.inputBar.input.returnPressed.connect(
            self.send_message
        )
            # ==========================================================
    # ADD MESSAGE
    # ==========================================================

    def add_message(self, text, sender):

        bubble = MessageBubble(text, sender)

        self.messages.addWidget(bubble)

        self.scroll_to_bottom()

    # ==========================================================
    # SEND MESSAGE
    # ==========================================================

    def send_message(self):

        text = self.inputBar.input.text().strip()

        if not text:
            return

        self.add_message(text, "user")

        self.inputBar.input.clear()

        self.typing = TypingIndicator()

        self.messages.addWidget(self.typing)

        self.scroll_to_bottom()

        self.worker = AIWorker(
            self.ai,
            text
        )

        self.worker.finished.connect(
            self.receive_ai
        )

        self.worker.start()

    # ==========================================================
    # RECEIVE AI
    # ==========================================================

    def receive_ai(self, reply):

        if hasattr(self, "typing"):

            self.messages.removeWidget(self.typing)

            self.typing.deleteLater()

        self.add_message(
            reply,
            "assistant"
        )

    # ==========================================================
    # AUTO SCROLL
    # ==========================================================

    def scroll_to_bottom(self):

        QTimer.singleShot(
            50,
            lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )
        )