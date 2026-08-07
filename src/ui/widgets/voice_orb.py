from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from PySide6.QtWidgets import QWidget


class VoiceOrb(QWidget):

    def __init__(self):

        super().__init__()

        self.setFixedSize(220, 220)

        self.pulse = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)      # ~60 FPS

    def animate(self):

        self.pulse += 1

        if self.pulse >= 360:
            self.pulse = 0

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()

        # -------------------------------------------------
        # Animated Pulse
        # -------------------------------------------------

        pulse = (self.pulse % 40) / 40

        radius = 55 + pulse * 12

        alpha = int(90 * (1 - pulse))

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(34, 211, 238, alpha))

        painter.drawEllipse(center, int(radius), int(radius))

        # -------------------------------------------------
        # Outer Ring
        # -------------------------------------------------

        pen = QPen(QColor("#22D3EE"))

        pen.setWidth(2)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(center, 74, 74)

        # -------------------------------------------------
        # Middle Ring
        # -------------------------------------------------

        pen = QPen(QColor("#38BDF8"))

        pen.setWidth(2)

        painter.setPen(pen)

        painter.drawEllipse(center, 60, 60)

        # -------------------------------------------------
        # Inner Glow
        # -------------------------------------------------

        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(QColor(34, 211, 238, 120)))

        painter.drawEllipse(center, 46, 46)

        painter.setBrush(QBrush(QColor("#22D3EE")))

        painter.drawEllipse(center, 34, 34)

        # -------------------------------------------------
        # AI Core
        # -------------------------------------------------

        painter.setBrush(QColor("#071018"))

        painter.drawEllipse(center, 18, 18)

        painter.setBrush(QColor("#FFFFFF"))

        painter.drawEllipse(center, 5, 5)