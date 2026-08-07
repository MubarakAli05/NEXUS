import sys

from PySide6.QtWidgets import QApplication

from src.ui.splash.splash_screen import SplashScreen


def main():

    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()