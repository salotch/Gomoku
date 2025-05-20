from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import sys

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace('\\', '/')

class Winner(QDialog):
    def __init__(self, parent=None, winner=None,isAi=False):
        super().__init__(parent)
        self.setWindowTitle("Winner")
        self.setFixedSize(780, 655)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
                border-radius: 15px;
                
            }
        """)
        self.setModal(True)
        self.choice = "exit"
        self.is_maximized = False
        self.old_pos = None
        self.winner = winner
        self.IsAI=isAi
        self.init_ui(winner)

    def init_ui(self, winner):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.background_label = QLabel(self)
        self.background_label.setStyleSheet("""
            QLabel {
                border-radius: 15px;
            }
        """)
        image_path = resource_path("assets/images/frame3/image.png")
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load background image '{image_path}'")
            self.setStyleSheet("""QDialog {
                    background-color: #222222;
                    border-radius: 15px;
                }""")
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            scaled_pixmap = pixmap.scaled(790, 687, Qt.AspectRatioMode.KeepAspectRatio)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.background_label.setGeometry(0,0, 790, 687)
                    
        if winner == "player1":
            overlay_path = resource_path("assets/images/frame3/playerWin1.png")
        elif winner == "player2":  
            overlay_path = resource_path("assets/images/frame3/playerWin2.png")
        else:
            overlay_path = resource_path("assets/images/frame3/Draw.png")
        overlay_image = QPixmap(overlay_path)
        if overlay_image.isNull():
            print(f"Error: Failed to load overlay image '{overlay_path}'")
        overlay_label = QLabel(self)
        overlay_label.setPixmap(overlay_image.scaled(440, 60, Qt.AspectRatioMode.KeepAspectRatio))
        x = (787 - overlay_image.width()) // 2
        overlay_label.setGeometry(x, 115, 440, 60)  
        overlay_label.raise_()

        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #3A393B;
                color: white;
                font-size: 16px;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(0)
        title_label = QLabel("Winner")
        title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        self.main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        if not self.IsAI:
            self.play_again_button = QPushButton("", self.content_widget)
            self.play_again_button.setFixedSize(314, 98)
            self.play_again_button.setGeometry(249, 330, 314, 98)
            playA_image=resource_path("assets/images/frame3/playAgain.png")
            self.play_again_button.setStyleSheet("""
                QPushButton {{
                    background-image: url("{0}");
                    background-color: transparent;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
                QPushButton:pressed {{
                    background-color: rgba(0, 0, 0, 0.2);
                }}
            """.format(playA_image))
            self.play_again_button.clicked.connect(lambda: self.select_choice("playAgain"))
        self.exit_button = QPushButton("", self.content_widget)
        self.exit_button.setFixedSize(200, 95)
        if self.IsAI:
            self.exit_button.setGeometry(300, 340, 200, 95)
        else:
            self.exit_button.setGeometry(300, 440, 200, 95)
        
        home_image=resource_path("assets/images/frame3/home.png")
        self.exit_button.setStyleSheet("""
            QPushButton {{
                background-image: url("{0}");
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """.format(home_image))
        self.exit_button.clicked.connect(self.back_home)
        self.content_layout.addStretch()
        self.title_bar.raise_()
        self.content_widget.raise_()

    def select_choice(self, choice):
        self.choice = choice
        self.accept()

    def get_choice(self):
        return self.choice

    def back_home(self):
        self.reject()  # Close the Winner dialog
        if self.parent():
            self.parent().reset_to_home()  # Calls reset_to_home on GomokuGame
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.geometry().contains(event.position().toPoint()):
            self.old_pos = event.globalPosition().toPoint()
            
    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

