import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
import pygame
from ChooseMode import Choice
from GUIboard import GameBoard
from GameEngine import GameEngine
from Player import AIAlphaBetaPruningPlayer, HumanPlayer, AIMinimaxPlayer
from Board import GomokuBoard, Board

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace('\\', '/')

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
            font-family: Rounded Mplus 1c;
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
        pixmap = QPixmap(resource_path("assets/images/frame0/home.png"))
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
        play_image = resource_path("assets/images/frame0/play.png")
        self.play_button.setStyleSheet("""
            QPushButton {{
                background-image: url("{0}");
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """.format(play_image))
        self.play_button.clicked.connect(self.play_function)
        button_layout.addWidget(self.play_button)
        self.help_button = QPushButton("", self.button_container)
        self.help_button.setFixedSize(274, 77)
        help_image = resource_path("assets/images/frame0/help.png")
        self.help_button.setStyleSheet("""
            QPushButton {{
                background-image: url("{0}");
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """.format(help_image))
        self.help_button.clicked.connect(self.help_function)
        button_layout.addWidget(self.help_button)
        self.content_layout.addWidget(self.button_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.content_layout.addStretch()
        self.sound_button = QPushButton(self.central_widget)
        self.sound_button.setFixedSize(40, 40)
        self.sound_button.setGeometry(1200, 730, 40, 40)
        self.sound_button.setIcon(QIcon(resource_path("assets/images/frame0/soundOn.png")))
        self.sound_button.setIconSize(QSize(40, 40))
        self.sound_button.setStyleSheet("background: transparent; border: none;")
        self.sound_button.clicked.connect(self.toggle_sound)
        self.sound_button.raise_()

    def setup_audio(self):
        self.background_music = pygame.mixer.Sound(resource_path("assets/audio/Cherry_Peace.mp3"))
        self.background_music.set_volume(0.25)
        self.background_music.play(-1)

    def toggle_sound(self):
        if self.is_playing:
            self.background_music.stop()
            self.sound_button.setIcon(QIcon(resource_path("assets/images/frame0/soundOff.png")))
            print("Sound is now off")
        else:
            self.background_music.play(-1)
            self.sound_button.setIcon(QIcon(resource_path("assets/images/frame0/soundOn.png")))
            print("Sound is now on")
        self.is_playing = not self.is_playing

    def play_function(self):
        dialog = Choice(self)
        if dialog.exec():
            choice = dialog.get_choice()
            if choice:
                self.update_home_content(choice)

    def help_function(self):
        print("Help button clicked")
        self.update_home_content("aiVSAI")

    def update_home_content(self, choice):
        for widget in self.content_widget.findChildren(QWidget):
            if widget != self.content_widget:
                widget.deleteLater()
        self.main_layout.removeWidget(self.content_widget)
        self.content_widget.deleteLater()
        self.content_widget = QWidget(self.central_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        if choice == "aiVSAI":
            self.game_board = GameBoard(self.content_widget, True)
        else:
            self.game_board = GameBoard(self.content_widget)
        self.game_board.setGeometry(0, 0, 1300, 800)
        self.game_board.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.game_board.raise_()
        self.game_board.show()
        
        board = GomokuBoard(15, 15)
        if choice == "2players":
            player1 = HumanPlayer('X', 'Player 1')
            player2 = HumanPlayer('O', 'Player 2')
        elif choice == "player&AI":
            player1 = HumanPlayer('X', 'Player 1')
            player2 = AIAlphaBetaPruningPlayer('O', 'AI', 1)
        else:
            player1 = AIMinimaxPlayer('X', 'AI', 1)
            player2 = AIAlphaBetaPruningPlayer('O', 'AI', 1)  
        self.gameEng = GameEngine(player1, player2, board)
        self.gameEng.playMoodGUI(choice, self.game_board)
        self.sound_button.raise_()
        self.sound_button.update()

    def reset_to_home(self):
        print("Resetting to home screen")
        if hasattr(self, 'gameEng') and self.gameEng:
            self.gameEng.stop_game()
        for widget in self.content_widget.findChildren(QWidget):
            if widget != self.content_widget:
                widget.deleteLater()
        self.main_layout.removeWidget(self.content_widget)
        self.content_widget.deleteLater()
        self.content_widget = QWidget(self.central_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        self.background_label = QLabel(self.content_widget)
        pixmap = QPixmap(resource_path("assets/images/frame0/home.png"))
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
        play_image = resource_path("assets/images/frame0/play.png")
        self.play_button.setStyleSheet("""
            QPushButton {{
                background-image: url("{0}");
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """.format(play_image))
        self.play_button.clicked.connect(self.play_function)
        button_layout.addWidget(self.play_button)
        self.help_button = QPushButton("", self.button_container)
        self.help_button.setFixedSize(274, 77)
        help_image = resource_path("assets/images/frame0/help.png")
        self.help_button.setStyleSheet("""
            QPushButton {{
                background-image: url("{0}");
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """.format(help_image))
        self.help_button.clicked.connect(self.help_function)
        button_layout.addWidget(self.help_button)
        self.content_layout.addWidget(self.button_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.content_layout.addStretch()
        self.sound_button.raise_()
        self.sound_button.update()
        self.content_widget.update()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None