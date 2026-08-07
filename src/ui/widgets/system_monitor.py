import psutil

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QWidget,
    QHBoxLayout,
)

from src.ui.widgets.glass_card import GlassCard
from src.ui.theme.colors import Colors


class SystemMonitor(GlassCard):

    def __init__(self):

        super().__init__("💻 System Status")

        # Card Size
        self.setMinimumHeight(220)
        self.setMaximumHeight(240)

        # Metrics
        self.cpu = self.create_metric("CPU")
        self.ram = self.create_metric("RAM")
        self.disk = self.create_metric("Disk")

        # Status
        self.status = QLabel("🟢 Everything is healthy")
        self.status.setStyleSheet(f"""
            color:{Colors.SUCCESS};
            font-size:13px;
            font-weight:600;
        """)

        self.content.addSpacing(4)
        self.content.addWidget(self.status)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

    # --------------------------------------------------

    def create_metric(self, name):

        row = QWidget()

        layout = QHBoxLayout(row)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel(name)

        title.setStyleSheet("""
            color:white;
            font-size:14px;
            font-weight:500;
        """)

        value = QLabel("0%")

        value.setAlignment(Qt.AlignRight)

        value.setStyleSheet(f"""
            color:{Colors.PRIMARY};
            font-size:14px;
            font-weight:700;
        """)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(value)

        bar = QProgressBar()

        bar.setMaximum(100)
        bar.setValue(0)
        bar.setTextVisible(False)
        bar.setFixedHeight(6)

        bar.setStyleSheet(f"""
        QProgressBar {{
            background:#0F172A;
            border:none;
            border-radius:3px;
        }}

        QProgressBar::chunk {{
            background:{Colors.PRIMARY};
            border-radius:3px;
        }}
        """)

        self.content.addWidget(row)
        self.content.addWidget(bar)
        self.content.addSpacing(8)

        return value, bar

    # --------------------------------------------------

    def update_stats(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        try:
            disk = psutil.disk_usage("/").percent
        except Exception:
            disk = psutil.disk_usage("C:\\").percent

        # CPU
        self.cpu[0].setText(f"{cpu:.0f}%")
        self.cpu[1].setValue(int(cpu))

        # RAM
        self.ram[0].setText(f"{ram:.0f}%")
        self.ram[1].setValue(int(ram))

        # Disk
        self.disk[0].setText(f"{disk:.0f}%")
        self.disk[1].setValue(int(disk))

        # Status Color
        if cpu > 90 or ram > 90:
            self.status.setText("🟠 High Resource Usage")
            self.status.setStyleSheet("""
                color:#F59E0B;
                font-size:13px;
                font-weight:600;
            """)
        else:
            self.status.setText("🟢 Everything is healthy")
            self.status.setStyleSheet(f"""
                color:{Colors.SUCCESS};
                font-size:13px;
                font-weight:600;
            """)