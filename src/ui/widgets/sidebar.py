from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from src.ui.widgets.sidebar_button import SidebarButton
from src.ui.widgets.status_chip import StatusChip


class Sidebar(QWidget):

    def __init__(self):

        super().__init__()

        self.setFixedWidth(240)

        self.setObjectName("Sidebar")

        self.setStyleSheet("""
        QWidget#Sidebar{
            background:#090E17;
            border-right:1px solid #182235;
        }
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 18, 20, 18)

        layout.setSpacing(0)

        # -------------------------------------------------
        # Logo Section
        # -------------------------------------------------

        logo = QLabel()

        pix = QPixmap("assets/logo/nexus_logo.png")

        if not pix.isNull():

            pix = pix.scaled(
                150,
                150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

        logo.setPixmap(pix)

        logo.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo)

        layout.addSpacing(12)

        # -------------------------------------------------
        # Divider
        # -------------------------------------------------

        line = QFrame()

        line.setFrameShape(QFrame.HLine)

        line.setStyleSheet("""
        background:#1C2738;
        max-height:1px;
        border:none;
        """)

        layout.addWidget(line)

        layout.addSpacing(20)

        # -------------------------------------------------
        # Navigation
        # -------------------------------------------------

        items = [

            ("Dashboard", "🏠", True),
            ("Chat", "💬", False),
            ("Voice", "🎤", False),
            ("Vision", "👁", False),
            ("Memory", "🧠", False),
            ("Automation", "⚙", False),
            ("Files", "📁", False),
            ("System", "💻", False),
            ("Settings", "⚙", False),

        ]

        for text, icon, active in items:

            button = SidebarButton(
                text,
                icon,
                active
            )

            layout.addWidget(button)

            layout.addSpacing(8)

        layout.addStretch()

        # -------------------------------------------------
        # Bottom Status
        # -------------------------------------------------

        layout.addWidget(StatusChip())