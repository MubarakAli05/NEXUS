import math
import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class BackgroundAnimation(QWidget):

    def __init__(self):

        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.phase = 0

        self.particles = []

        # Create particles
        for _ in range(260):

            self.particles.append({

                "x": random.uniform(0, 1),

                "offset": random.uniform(-25, 25),

                "speed": random.uniform(0.8, 1.5),

                "size": random.uniform(1.5, 3.5),

            })

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)

    # ---------------------------------------------------

    def animate(self):

        self.phase += 0.035

        self.update()

    # ---------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()

        h = self.height()

        center = h / 2

        for p in self.particles:

            x = p["x"] * w

            y = (
                center
                + math.sin((x * 0.018) + self.phase * p["speed"]) * 20
                + p["offset"]
            )

            alpha = int(
                70 +
                80 *
                (
                    0.5 +
                    0.5 *
                    math.sin(self.phase * 2 + x * 0.01)
                )
            )

            painter.setBrush(
                QColor(
                    34,
                    211,
                    238,
                    alpha
                )
            )

            painter.setPen(Qt.PenStyle.NoPen)

            s = p["size"]

            painter.drawEllipse(
                int(x),
                int(y),
                int(s),
                int(s)
            )