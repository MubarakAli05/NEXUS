from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)


class MessageBubble(QWidget):

    def __init__(self, message, sender="assistant"):

        super().__init__()

        outer = QHBoxLayout(self)

        outer.setContentsMargins(0, 4, 0, 4)

        # -------------------------------------------------
        # Bubble
        # -------------------------------------------------

        bubble = QFrame()

        bubble.setMaximumWidth(700)

        layout = QVBoxLayout(bubble)

        layout.setContentsMargins(18, 14, 18, 14)

        layout.setSpacing(8)

        # -------------------------------------------------
        # Sender
        # -------------------------------------------------

        senderLabel = QLabel()

        if sender == "user":

            senderLabel.setText("You")

            bubble.setStyleSheet("""
            QFrame{
                background:#22D3EE;
                border-radius:16px;
            }
            """)

            senderLabel.setStyleSheet("""
                color:black;
                font-size:12px;
                font-weight:700;
            """)

        else:

            senderLabel.setText("NEXUS")

            bubble.setStyleSheet("""
            QFrame{
                background:#162133;
                border:1px solid #243247;
                border-radius:16px;
            }
            """)

            senderLabel.setStyleSheet("""
                color:#22D3EE;
                font-size:12px;
                font-weight:700;
            """)

        # -------------------------------------------------
        # Message
        # -------------------------------------------------

        body = QLabel(message)

        body.setWordWrap(True)

        body.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        if sender == "user":

            body.setStyleSheet("""
                color:black;
                font-size:15px;
                line-height:150%;
            """)

        else:

            body.setStyleSheet("""
                color:white;
                font-size:15px;
                line-height:150%;
            """)

        layout.addWidget(senderLabel)

        layout.addWidget(body)

        # -------------------------------------------------
        # Alignment
        # -------------------------------------------------

        if sender == "user":

            outer.addStretch()

            outer.addWidget(bubble)

        else:

            outer.addWidget(bubble)

            outer.addStretch()