from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt,QSize
import pygame
import os
import sys

class GameBoard(QWidget):
    def __init__(self, parent=None,isAI=False):
        super().__init__(parent)
        self.cell_size = 40
        self.grid_size = 15
        self.black_stone_icon = QIcon(resource_path("assets/images/frame2/bStone.png"))
        self.red_stone_icon = QIcon(resource_path("assets/images/frame2/rStone.png"))
        self.icon_size = QSize(self.cell_size, self.cell_size)
        self.offset_x = 77
        self.offset_y = 52
        self.setFixedSize(1300, 800)
        self.buttons = {}
        self.score1=0
        self.score2=0
        self.engine = None
        self.isAIvsAI=isAI
        print("Class initiated")
        self.init_board()
        pygame.mixer.init()

    def init_board(self):
        background_label = QLabel(self)
        if(self.isAIvsAI):
            path = resource_path("assets/images/frame4/board.png")
        else:
            path = resource_path("assets/images/frame2/board.png")
            #score above the background
            self.text_label = QLabel(str(self.score1), self)
            self.text_label.setStyleSheet("""
                color: #3A393A;
                font-size: 40px;
                font-weight: bold;
                background-color:transparent;
                font-family:Rounded Mplus 1c Bold;  
            """)
            self.text_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.text_label.setGeometry(933,578,25,45)
            self.text_label.raise_()

            self.text_label1 = QLabel(str(self.score2), self)
            self.text_label1.setStyleSheet("""
                color: #3A393A;
                font-size: 40px;
                font-weight: bold;
                background-color:transparent;
                font-family:Rounded Mplus 1c Bold;  
            """)
            self.text_label1.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.text_label1.setGeometry(1126,578,25,45)
            self.text_label1.raise_()
        pixmap=QPixmap(path)
        if pixmap.isNull():
            print(f"Error: Failed to load background image '{path}'")
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            background_label.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
        background_label.setGeometry(0, 0, self.width(), self.height())
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = QPushButton(self)
                button.setFixedSize(self.cell_size, self.cell_size)
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
                if col > 0:
                    x += 7 * col
                if row > 0:
                    y += 7 * row
                button.setGeometry(x, y, self.cell_size, self.cell_size)
                button.setStyleSheet("background: transparent; border: none;")
                button.clicked.connect(lambda checked, r=row, c=col, b=button: self.button_clicked(r, c, b))
                self.buttons[(row, col)] = button
        print("Board initiated")

    def button_clicked(self, row, col, button):
        if self.engine:
            self.engine.process_move(row, col, button)
            self.setup_audio()

    def set_engine(self, engine):
        self.engine = engine

    def disable_board(self):
        for button in self.buttons.values():
            button.setEnabled(False)

    def enable_board(self):
        for button in self.buttons.values():
            button.setEnabled(True)

    def setup_audio(self):
        self.background_music = pygame.mixer.Sound(resource_path("assets/audio/mouse-click.mp3"))
        self.background_music.set_volume(0.5)
        self.background_music.play(0)
    
    def update_text(self, score1,score2):
        print("updating the score")
        if self.text_label:
            self.score1+=score1
            self.text_label.setText(str(self.score1))
        if self.text_label1:
            self.score2+=score2
            self.text_label1.setText(str(self.score2))
        
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace('\\', '/')
            