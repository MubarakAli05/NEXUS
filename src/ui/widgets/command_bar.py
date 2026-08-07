from PySide6.QtWidgets import QLineEdit

from src.ui.theme.styles import Styles


class CommandBar(QLineEdit):

    def __init__(self):

        super().__init__()

        self.setPlaceholderText("> Ask NEXUS anything...")

        self.setMinimumHeight(58)

        self.setStyleSheet(Styles.SEARCH)