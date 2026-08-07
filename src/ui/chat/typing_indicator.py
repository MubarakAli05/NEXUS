from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QFrame,
    QVBoxLayout,
)


class TypingIndicator(QWidget):

    def __init__(self):

        super().__init__()

        outer = QHBoxLayout(self)

        outer.setContentsMargins(0, 4, 0, 4)

        bubble = QFrame()

        bubble.setStyleSheet("""
        QFrame{
            background:#162133;
            border:1px solid #243247;
            border-radius:16px;
        }
        """)

        layout = QVBoxLayout(bubble)

        layout.setContentsMargins(18,14,18,14)

        title = QLabel("NEXUS")

        title.setStyleSheet("""
            color:#22D3EE;
            font-size:12px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        dots = QHBoxLayout()

        self.labels = []

        for _ in range(3):

            dot = QLabel("●")

            dot.setStyleSheet("""
                color:#3A4B63;
                font-size:18px;
            """)

            dots.addWidget(dot)

            self.labels.append(dot)

        dots.addStretch()

        layout.addLayout(dots)

        outer.addWidget(bubble)

        outer.addStretch()

        self.index = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(300)

    # -----------------------------------

    def animate(self):

        for i, dot in enumerate(self.labels):

            if i == self.index:

                dot.setStyleSheet("""
                    color:#22D3EE;
                    font-size:18px;
                """)

            else:

                dot.setStyleSheet("""
                    color:#3A4B63;
                    font-size:18px;
                """)

        self.index = (self.index + 1) % 3