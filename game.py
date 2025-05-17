import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
import pygame
import os
from ChooseMode import Choice
from GUIboard import GameBoard
from GameEngine import GameEngine
from Player import AIAlphaBetaPruningPlayer, Player, HumanPlayer, AIMinimaxPlayer
from Board import GomokuBoard, Board


class GomokuGame(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gomoku")
        self.setFixedSize(1300, 830)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.init_ui()
        pygame.mixer.init()
        self.old_pos = None
        self.is_playing = True
        self.setup_audio()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.title_bar = QWidget(self.central_widget)
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            background-color: #3A393B;
            color: white;
            font-family:Rounded Mplus 1c;
            font-size: 16px;
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(0)
        title_label = QLabel("Gomoku")
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
            QPushButton:hover {
                background-color: #555555;
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
        self.close_button.clicked.connect(self.close)
        title_layout.addWidget(self.close_button)
        self.main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self.central_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        self.background_label = QLabel(self.content_widget)
        pixmap = QPixmap("assets/images/frame0/home.png")
        if pixmap.isNull():
            print("Error: Failed to load background image 'assets/images/frame0/home.png'")
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            self.background_label.setPixmap(pixmap.scaled(1333, 820, Qt.AspectRatioMode.KeepAspectRatio))
        self.background_label.setGeometry(0, 0, 1333, 820)
        self.content_layout.addSpacerItem(QSpacerItem(20, 400, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.content_layout.addStretch()
        self.button_container = QWidget(self.content_widget)
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        self.button_container.setLayout(button_layout)
        self.play_button = QPushButton("", self.button_container)
        self.play_button.setFixedSize(274, 77)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame0/play.png);
                background-color: transparent;
                border: none;
                border-radius:20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.play_button.clicked.connect(self.play_function)
        button_layout.addWidget(self.play_button)
        self.help_button = QPushButton("", self.button_container)
        self.help_button.setFixedSize(274, 77)
        self.help_button.setStyleSheet("""
            QPushButton {
                background-image: url(assets/images/frame0/help.png);
                background-color: transparent;
                border: none;
                border-radius:20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.help_button.clicked.connect(self.help_function)
        button_layout.addWidget(self.help_button)
        self.content_layout.addWidget(self.button_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.content_layout.addStretch()
        self.sound_button = QPushButton(self.central_widget)
        self.sound_button.setFixedSize(40, 40)
        self.sound_button.setGeometry(1200, 730, 40, 40)
        self.sound_button.setIcon(QIcon("assets/images/frame0/soundOn.png"))
        self.sound_button.setIconSize(QSize(40, 40))
        self.sound_button.setStyleSheet("background: transparent; border: none;")
        self.sound_button.clicked.connect(self.toggle_sound)
        self.sound_button.raise_()  # Ensure sound button is initially on top

    def setup_audio(self):
       
        try:
            music_path = os.path.join("assets", "audio", "Cherry_Peace.mp3")
            if not os.path.exists(music_path):
                print(f"Error: Audio file not found at {music_path}")
                return
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            if self.is_playing:
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error initializing audio: {str(e)}")

    def toggle_sound(self):
        self.is_playing = not self.is_playing
        icon = QIcon("assets/images/frame0/soundOn.png" if self.is_playing else "assets/images/frame0/soundOff.png")
        self.sound_button.setIcon(QIcon(icon))
        if self.is_playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        print(f"Sound is now {'on' if self.is_playing else 'off'}")

    def play_function(self):
        dialog = Choice(self)
        if dialog.exec():
            choice = dialog.get_choice()
            if choice == "2players":
                player1 = HumanPlayer('X', 'Player 1')
                player2 = HumanPlayer('O', 'Player 2')
            elif choice == "player&AI":
                player1 = HumanPlayer('X', 'Player 1')
                player2 = AIMinimaxPlayer('O', 'AI')
            self.gameEng = GameEngine(player1, player2, GomokuBoard(15, 15))
            self.update_home_content(choice)
        print("Play button clicked")

    def update_home_content(self, choice):
        print("Starting update_home_content")
        for widget in self.content_widget.findChildren(QWidget):
            if widget != self.content_widget:
                widget.deleteLater()
        self.main_layout.removeWidget(self.content_widget)
        self.content_widget.deleteLater()
        self.content_widget = QWidget(self.central_widget)
        self.main_layout.addWidget(self.content_widget)
        print("New content_widget created")
        self.background_label = QLabel(self.content_widget)
        pixmap = QPixmap("assets/images/frame2/board.png")
        if pixmap.isNull():
            print("Failed to load board image.")
        else:
            print(f"Loaded board image: {pixmap.width()}x{pixmap.height()}")
            self.background_label.setPixmap(pixmap.scaled(1300, 800, Qt.AspectRatioMode.KeepAspectRatio))
            self.background_label.setGeometry(0, 0, 1300, 800)
            self.background_label.lower()
        print("Background label set")
        self.game_board = GameBoard(self.content_widget)
        self.game_board.setGeometry(0, 0, 1300, 800)
        self.game_board.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.game_board.raise_()
        self.game_board.show()
        self.gameEng.playMoodGUI(choice, self.game_board)
        self.sound_button.raise_()  # Ensure sound button is on top
        self.sound_button.update()  # Force redraw
        self.content_widget.update()
        self.update()
        print(f"GameBoard geometry: {self.game_board.geometry()}")
        print("Completed update_home_content")

    def help_function(self):
        player1 = AIMinimaxPlayer('X', 'Minimax AI',1)
        player2 = AIAlphaBetaPruningPlayer('O', 'Alpha-Beta AI',1)
        self.gameEng = GameEngine(player1, player2, GomokuBoard(15, 15))
        for widget in self.content_widget.findChildren(QWidget):
            if widget != self.content_widget:
                widget.deleteLater()
        self.main_layout.removeWidget(self.content_widget)
        self.content_widget.deleteLater()
        self.content_widget = QWidget(self.central_widget)
        self.main_layout.addWidget(self.content_widget)
        self.background_label = QLabel(self.content_widget)
        pixmap = QPixmap("assets/images/frame4/board.png")
        if pixmap.isNull():
            print("Failed to load board image.")
        else:
            self.background_label.setPixmap(pixmap.scaled(1300, 800, Qt.AspectRatioMode.KeepAspectRatio))
            self.background_label.setGeometry(0, 0, 1300, 800)
            self.background_label.lower()
        self.game_board = GameBoard(self.content_widget)
        self.game_board.setGeometry(0, 0, 1300, 800)
        self.game_board.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.game_board.raise_()
        self.game_board.show()
        QTimer.singleShot(100,lambda:self.gameEng.playMoodGUI("aiVSAI",self.game_board))
        self.sound_button.raise_()  # Ensure sound button is on top
        self.sound_button.update()  # Force redraw
        self.content_widget.update()
        self.update()
        print("Help button clicked")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GomokuGame()
    window.show()
    sys.exit(app.exec())