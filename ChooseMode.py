from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class Choice(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Mode")
        self.setFixedSize(780, 655)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.choice = "2players"
        self.is_maximized = False
        self.old_pos = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.background_label = QLabel(self)
        image_path = "assets/images/frame1/image.png"
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load background image '{image_path}'")
            self.setStyleSheet("background-color: #222222;")
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            scaled_pixmap = pixmap.scaled(780, 655, Qt.AspectRatioMode.KeepAspectRatio)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.background_label.setGeometry(0, 0, 780, 655)
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("""
            background-color: #3A393B;
            color: white;
            font-size: 16px;
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(0)
        title_label = QLabel("Game Mode")
        title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.minimize_button)
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)
        self.close_button.clicked.connect(self.reject)
        title_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        self.single_button = QPushButton("", self.content_widget)
        self.single_button.setFixedSize(310, 107)
        self.single_button.setGeometry(60, 380, 310, 107)
        self.single_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame1/2players.png);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.single_button.clicked.connect(lambda: self.select_choice("2players"))
        self.multi_button = QPushButton("", self.content_widget)
        self.multi_button.setFixedSize(359, 107)
        self.multi_button.setGeometry(375, 380, 359, 107)
        self.multi_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame1/playerVS.png);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.multi_button.clicked.connect(lambda: self.select_choice("player&AI"))
        self.content_layout.addStretch()
        self.title_bar.raise_()
        self.content_widget.raise_()

    def select_choice(self, choice):
        self.choice = choice
        self.accept()

    def get_choice(self):
        return self.choice

class Winner(QDialog):
    def __init__(self, parent=None, winner=None):
        super().__init__(parent)
        self.setWindowTitle("Winner")
        self.setFixedSize(780, 655)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.choice = "exit"
        self.is_maximized = False
        self.old_pos = None
        self.winner = winner
        self.init_ui(winner)

    def init_ui(self, winner):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.background_label = QLabel(self)
        image_path = "assets/images/frame3/image.png"
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load background image '{image_path}'")
            self.setStyleSheet("background-color: #222222;")
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            scaled_pixmap = pixmap.scaled(790, 687, Qt.AspectRatioMode.KeepAspectRatio)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.background_label.setGeometry(0, 0, 790, 687)
        
        if winner == "player1":
            overlay_path = "assets/images/frame3/playerWin1.png"
        elif winner =="player2":  
            overlay_path = "assets/images/frame3/playerWin2.png"
        else:
            overlay_path ="assets/images/frame3/Draw.png"
        overlay_image = QPixmap(overlay_path)
        if overlay_image.isNull():
            print(f"Error: Failed to load overlay image '{overlay_path}'")
        overlay_label = QLabel(self)
        overlay_label.setPixmap(overlay_image.scaled(440, 60, Qt.AspectRatioMode.KeepAspectRatio))
        x = (787 - overlay_image.width())//2
        overlay_label.setGeometry(x, 115, 440, 60)  
        overlay_label.raise_()

        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("""
            background-color: #3A393B;
            color: white;
            font-size: 16px;
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(0)
        title_label = QLabel("Winner")
        title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.minimize_button)
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)
        self.close_button.clicked.connect(self.reject)
        title_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        self.play_again_button = QPushButton("", self.content_widget)
        self.play_again_button.setFixedSize(314, 98)
        self.play_again_button.setGeometry(249, 330, 314, 98)
        self.play_again_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame3/playAgain.png);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.play_again_button.clicked.connect(lambda: self.select_choice("playAgain"))
        self.exit_button = QPushButton("", self.content_widget)
        self.exit_button.setFixedSize(200, 95)
        self.exit_button.setGeometry(300, 440, 200, 95)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame3/exit.png);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.exit_button.clicked.connect(self.reject)
        self.content_layout.addStretch()
        self.title_bar.raise_()
        self.content_widget.raise_()

    def select_choice(self, choice):
        self.choice = choice
        self.accept()

    def get_choice(self):
        return self.choice
    
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # # To test Choice dialog
    # dialog = Choice()
    # if dialog.exec():
    #     print("Choice selected:", dialog.get_choice())

    # To test Winner dialog (uncomment the lines below)
    winner_dialog = Winner(winner="Draw")  # or "Player 2"
    if winner_dialog.exec():
        print("Winner choice:", winner_dialog.get_choice())

    sys.exit(app.exec())
