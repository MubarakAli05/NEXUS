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
# AI STREAM WORKER
# ==========================================================

class AIWorker(QThread):

    chunk_received = Signal(str)

    finished = Signal()

    error = Signal(str)

    def __init__(self, ai, message):

        super().__init__()

        self.ai = ai

        self.message = message

    def run(self):

        try:

            for chunk in self.ai.ask_stream(
                self.message
            ):

                self.chunk_received.emit(chunk)

            self.finished.emit()

        except Exception as e:

            self.error.emit(str(e))


# ==========================================================
# CHAT AREA
# ==========================================================

class ChatArea(QWidget):

    def __init__(self):

        super().__init__()

        # ==================================================
        # AI
        # ==================================================

        self.ai = AIEngine()

        self.worker = None

        self.current_bubble = None

        # ==================================================
        # WINDOW
        # ==================================================

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

        self.main.setContentsMargins(
            24,
            20,
            24,
            20
        )

        self.main.setSpacing(18)

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        title = QLabel(
            "💬 NEXUS Assistant"
        )

        title.setStyleSheet("""
            font-size:24px;
            font-weight:700;
            color:white;
        """)

        self.status = QLabel(
            "🟢 Online"
        )

        self.status.setStyleSheet("""
            color:#22C55E;
            font-size:14px;
            font-weight:600;
        """)

        header.addWidget(title)

        header.addStretch()

        header.addWidget(
            self.status
        )

        self.main.addLayout(header)

        # ==================================================
        # CHAT SCROLL
        # ==================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        container = QWidget()

        self.messages = QVBoxLayout(
            container
        )

        self.messages.setAlignment(
            Qt.AlignTop
        )

        self.messages.setSpacing(
            14
        )

        self.messages.setContentsMargins(
            0,
            10,
            0,
            10
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

        self.scroll.setWidget(
            container
        )

        self.main.addWidget(
            self.scroll,
            1
        )

        # ==================================================
        # INPUT BAR
        # ==================================================

        self.inputBar = InputBar()

        self.main.addWidget(
            self.inputBar
        )

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

    def add_message(
        self,
        text,
        sender
    ):

        bubble = MessageBubble(
            text,
            sender
        )

        self.messages.addWidget(
            bubble
        )

        self.scroll_to_bottom()

        return bubble

    # ==========================================================
    # SEND MESSAGE
    # ==========================================================

    def send_message(self):

        # Prevent multiple requests
        if (
            self.worker is not None
            and self.worker.isRunning()
        ):
            return

        text = (
            self.inputBar.input
            .text()
            .strip()
        )

        if not text:
            return

        # --------------------------------------------------
        # USER MESSAGE
        # --------------------------------------------------

        self.add_message(
            text,
            "user"
        )

        self.inputBar.input.clear()

        # --------------------------------------------------
        # TYPING INDICATOR
        # --------------------------------------------------

        self.typing = TypingIndicator()

        self.messages.addWidget(
            self.typing
        )

        self.scroll_to_bottom()

        # --------------------------------------------------
        # WORKER
        # --------------------------------------------------

        self.worker = AIWorker(
            self.ai,
            text
        )

        self.worker.chunk_received.connect(
            self.receive_chunk
        )

        self.worker.finished.connect(
            self.receive_finished
        )

        self.worker.error.connect(
            self.receive_error
        )

        self.worker.start()

        # --------------------------------------------------
        # INPUT STATE
        # --------------------------------------------------

        self.inputBar.input.setEnabled(
            False
        )

        self.inputBar.send.setEnabled(
            False
        )



    def receive_chunk(self, chunk):

    # ==================================================
    # FIRST CHUNK
    # ==================================================

        if self.current_bubble is None:

            # Remove typing indicator

            if hasattr(self, "typing"):

                self.messages.removeWidget(
                    self.typing
                )

                self.typing.deleteLater()

                self.typing = None

            # Create empty NEXUS bubble

            self.current_bubble = MessageBubble(
                "",
                "assistant"
            )

            self.messages.addWidget(
                self.current_bubble
            )

            self.current_response = ""

        # ==================================================
        # APPEND CHUNK
        # ==================================================

        self.current_response += chunk

        # Update existing QLabel

        self.current_bubble.set_message(
            self.current_response
        )

        QTimer.singleShot(
            30,
            self.scroll_to_bottom
        )
        # --------------------------------------------------
        # Update bubble
        # --------------------------------------------------

        current_text = getattr(
            self.current_bubble,
            "text",
            ""
        )

        current_text += chunk

        # --------------------------------------------------
        # Try common QLabel-based bubble APIs
        # --------------------------------------------------

        if hasattr(
            self.current_bubble,
            "label"
        ):

            self.current_bubble.label.setText(
                current_text
            )

        elif hasattr(
            self.current_bubble,
            "message"
        ):

            self.current_bubble.message.setText(
                current_text
            )

        elif hasattr(
            self.current_bubble,
            "setText"
        ):

            self.current_bubble.setText(
                current_text
            )

        else:

            # Fallback:
            # recreate bubble text

            self.messages.removeWidget(
                self.current_bubble
            )

            self.current_bubble.deleteLater()

            self.current_bubble = MessageBubble(
                current_text,
                "assistant"
            )

            self.messages.addWidget(
                self.current_bubble
            )

        # Store text for next chunk

        self.current_bubble.text = current_text

        self.scroll_to_bottom()

    # ==========================================================
    # AI FINISHED
    # ==========================================================

    def receive_finished(self):

        # Remove typing indicator if
        # response somehow finished empty.

        if hasattr(
            self,
            "typing"
        ):

            if self.typing is not None:

                self.messages.removeWidget(
                    self.typing
                )

                self.typing.deleteLater()

                self.typing = None

        self.current_bubble = None

        self.worker = None

        # Enable input again

        self.inputBar.input.setEnabled(
            True
        )

        self.inputBar.send.setEnabled(
            True
        )

        self.inputBar.input.setFocus()

        self.scroll_to_bottom()

    # ==========================================================
    # AI ERROR
    # ==========================================================

    def receive_error(
        self,
        error_message
    ):

        if hasattr(
            self,
            "typing"
        ):

            self.messages.removeWidget(
                self.typing
            )

            self.typing.deleteLater()

            self.typing = None

        self.current_bubble = None

        self.worker = None

        self.add_message(
            "⚠️ NEXUS couldn't connect to the AI.\n\n"
            f"Error: {error_message}",
            "assistant"
        )

        self.inputBar.input.setEnabled(
            True
        )

        self.inputBar.send.setEnabled(
            True
        )

        self.inputBar.input.setFocus()

    # ==========================================================
    # AUTO SCROLL
    # ==========================================================

    def scroll_to_bottom(self):

        QTimer.singleShot(
            30,
            lambda: self.scroll
            .verticalScrollBar()
            .setValue(
                self.scroll
                .verticalScrollBar()
                .maximum()
            )
        )