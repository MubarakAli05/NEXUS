from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from src.ui.theme.colors import Colors
from src.ui.theme.spacing import Spacing
from src.ui.theme.radius import Radius
from src.ui.theme.typography import Font


class GlassCard(QFrame):

    def __init__(self, title=""):

        super().__init__()

        self.setObjectName("GlassCard")

        

        self.setStyleSheet(f"""
        QFrame#GlassCard{{

            background:qlineargradient(
                x1:0,
                y1:0,
                x2:0,
                y2:1,
                stop:0 #162133,
                stop:1 #111827
            );

            border:1px solid #243247;

            border-radius:{Radius.CARD}px;
        }}

        QFrame#GlassCard:hover{{

            border:1px solid {Colors.PRIMARY};

            background:qlineargradient(
                x1:0,
                y1:0,
                x2:0,
                y2:1,
                stop:0 #1B2940,
                stop:1 #131D2D
            );

        }}
        """)

        # -------------------------
        # Shadow
        # -------------------------

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(28)

        shadow.setOffset(0, 8)

        shadow.setColor(QColor(0, 0, 0, 120))

        self.setGraphicsEffect(shadow)

        # -------------------------
        # Layout
        # -------------------------

        self.main = QVBoxLayout(self)

        self.main.setContentsMargins(
            24,
            22,
            24,
            22,
        )

        self.main.setSpacing(10)

        if title:

            header = QLabel(title)

            header.setAlignment(Qt.AlignLeft)

            header.setStyleSheet(f"""
                color:{Colors.TEXT};

                font-size:{Font.CARD_TITLE}px;

                font-weight:700;
            """)

            self.main.addWidget(header)

            self.main.addSpacing(4)

        self.content = QVBoxLayout()

        self.content.setSpacing(10)

        self.main.addLayout(self.content)
