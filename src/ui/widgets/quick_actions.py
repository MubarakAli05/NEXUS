import subprocess
import os

from PySide6.QtWidgets import QGridLayout

from src.ui.widgets.glass_card import GlassCard
from src.ui.widgets.glow_button import GlowButton


class QuickActions(GlassCard):

    def __init__(self):

        super().__init__("⚡ Quick Actions")

        self.setMaximumHeight(220)

        grid = QGridLayout()

        grid.setContentsMargins(0, 0, 0, 0)

        grid.setHorizontalSpacing(14)

        grid.setVerticalSpacing(14)

        actions = [
            ("VS Code", "💻", self.vscode),
            ("Browser", "🌐", self.browser),
            ("Downloads", "📁", self.downloads),
            ("Terminal", "🖥", self.terminal),
        ]

        row = 0
        col = 0

        for text, icon, func in actions:

            button = GlowButton(text, icon)

            button.clicked.connect(func)

            grid.addWidget(button, row, col)

            col += 1

            if col == 2:
                col = 0
                row += 1

        self.content.addLayout(grid)

    def browser(self):
        os.startfile("https://google.com")

    def downloads(self):
        os.startfile(
            os.path.join(
                os.path.expanduser("~"),
                "Downloads",
            )
        )

    def terminal(self):
        subprocess.Popen("start cmd", shell=True)

    def vscode(self):
        subprocess.Popen("code", shell=True)