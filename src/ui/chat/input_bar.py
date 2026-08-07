from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class InputBar(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("InputBar")

        self.setStyleSheet("""
        QWidget#InputBar{
            background:#090E17;
        }

        QLineEdit{
            background:#111827;
            border:1px solid #243247;
            border-radius:14px;
            color:white;
            padding:14px;
            font-size:15px;
        }

        QLineEdit:focus{
            border:1px solid #22D3EE;
        }

        QPushButton{
            background:#162133;
            border:1px solid #243247;
            border-radius:12px;
            color:white;
            font-size:18px;
        }

        QPushButton:hover{
            background:#1E293B;
            border:1px solid #22D3EE;
        }
        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(10)

        # -------------------------------------

        self.attach = QPushButton("📎")

        self.attach.setFixedSize(46, 46)

        layout.addWidget(self.attach)

        # -------------------------------------

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Ask NEXUS anything..."
        )

        self.input.setMinimumHeight(46)

        layout.addWidget(self.input, 1)

        # -------------------------------------

        self.voice = QPushButton("🎤")

        self.voice.setFixedSize(46, 46)

        layout.addWidget(self.voice)

        # -------------------------------------

        self.send = QPushButton("➜")

        self.send.setFixedSize(46, 46)

        self.send.setStyleSheet("""
        QPushButton{
            background:#22D3EE;
            color:black;
            border:none;
            border-radius:12px;
            font-size:18px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#38BDF8;
        }
        """)

        layout.addWidget(self.send)