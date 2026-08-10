from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)


class MessageBubble(QWidget):

    def __init__(
        self,
        message="",
        sender="assistant"
    ):

        super().__init__()

        self.sender = sender

        # ==================================================
        # OUTER LAYOUT
        # ==================================================

        outer = QHBoxLayout(self)

        outer.setContentsMargins(
            0,
            4,
            0,
            4,
        )

        # ==================================================
        # BUBBLE
        # ==================================================

        self.bubble = QFrame()

        self.bubble.setMaximumWidth(700)

        layout = QVBoxLayout(
            self.bubble
        )

        layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        layout.setSpacing(8)

        # ==================================================
        # SENDER
        # ==================================================

        self.senderLabel = QLabel()

        if sender == "user":

            self.senderLabel.setText(
                "You"
            )

            self.bubble.setStyleSheet("""
            QFrame{
                background:#22D3EE;
                border-radius:16px;
            }
            """)

            self.senderLabel.setStyleSheet("""
                color:black;
                font-size:12px;
                font-weight:700;
            """)

        else:

            self.senderLabel.setText(
                "NEXUS"
            )

            self.bubble.setStyleSheet("""
            QFrame{
                background:#162133;
                border:1px solid #243247;
                border-radius:16px;
            }
            """)

            self.senderLabel.setStyleSheet("""
                color:#22D3EE;
                font-size:12px;
                font-weight:700;
            """)

        # ==================================================
        # MESSAGE BODY
        # ==================================================

        self.body = QLabel(
            message
        )

        self.body.setWordWrap(
            True
        )

        self.body.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        if sender == "user":

            self.body.setStyleSheet("""
                color:black;
                font-size:15px;
            """)

        else:

            self.body.setStyleSheet("""
                color:white;
                font-size:15px;
            """)

        # ==================================================
        # ADD CONTENT
        # ==================================================

        layout.addWidget(
            self.senderLabel
        )

        layout.addWidget(
            self.body
        )

        # ==================================================
        # ALIGNMENT
        # ==================================================

        if sender == "user":

            outer.addStretch()

            outer.addWidget(
                self.bubble
            )

        else:

            outer.addWidget(
                self.bubble
            )

            outer.addStretch()

    # ==========================================================
    # UPDATE MESSAGE
    # ==========================================================

    def set_message(
        self,
        message
    ):

        self.body.setText(
            message
        )

        self.body.adjustSize()

        self.bubble.adjustSize()

        self.adjustSize()