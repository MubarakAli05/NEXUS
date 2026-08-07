from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
)
from PySide6.QtGui import (
    QFont,
    QPixmap,
)
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QGraphicsOpacityEffect,
)

from src.ui.dashboard.dashboard import Dashboard


class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.dashboard = None

        self.progress_value = 0

        self.setWindowTitle("NEXUS")

        self.setFixedSize(700, 400)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("""
        QWidget{
            background:#090E17;
        }

        QLabel{
            color:white;
            background:transparent;
        }
        """)

        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignCenter)

        layout.setSpacing(15)

        # ---------------- Logo ----------------

        self.logo = QLabel()

        pixmap = QPixmap("assets/logo/nexus_logo.png")

        pixmap = pixmap.scaled(
            220,
            220,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.logo.setPixmap(pixmap)

        self.logo.setAlignment(Qt.AlignCenter)

        # ---------------- Title ----------------

        title = QLabel("NEXUS")

        title.setAlignment(Qt.AlignCenter)

        title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        # ---------------- Subtitle ----------------

        self.subtitle = QLabel("Initializing AI Core...")

        self.subtitle.setAlignment(Qt.AlignCenter)

        self.subtitle.setFont(QFont("Segoe UI", 11))

        self.subtitle.setStyleSheet("color:#94A3B8;")

        # ---------------- Progress ----------------

        self.progress = QProgressBar()

        self.progress.setFixedWidth(300)

        self.progress.setMaximum(100)

        self.progress.setTextVisible(False)

        self.progress.setStyleSheet("""
        QProgressBar{
            background:#111827;
            border:none;
            border-radius:5px;
            height:8px;
        }

        QProgressBar::chunk{
            background:#22D3EE;
            border-radius:5px;
        }
        """)

        layout.addStretch()

        layout.addWidget(self.logo)

        layout.addWidget(title)

        layout.addWidget(self.subtitle)

        layout.addSpacing(10)

        layout.addWidget(
            self.progress,
            alignment=Qt.AlignCenter
        )

        layout.addStretch()

        # ---------------- Fade In ----------------

        effect = QGraphicsOpacityEffect()

        self.setGraphicsEffect(effect)

        self.animation = QPropertyAnimation(effect, b"opacity")

        self.animation.setDuration(1200)

        self.animation.setStartValue(0)

        self.animation.setEndValue(1)

        self.animation.start()

        # ---------------- Loading Timer ----------------

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_progress)

        self.timer.start(30)

    def update_progress(self):

        self.progress_value += 1

        self.progress.setValue(self.progress_value)

        if self.progress_value >= 100:

            self.timer.stop()

            self.open_dashboard()

    def open_dashboard(self):

        self.dashboard = Dashboard()

        self.dashboard.showMaximized()

        self.close()