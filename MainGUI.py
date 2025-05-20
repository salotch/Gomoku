import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from game import GomokuGame  
import os

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace('\\', '/')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icon.ico")))  # Optional: Set window icon
    game = GomokuGame()  # Replace with your main game class
    game.show()
    sys.exit(app.exec())