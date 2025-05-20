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

class Choice(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Mode")
        self.setFixedSize(780, 655)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
                border-radius: 15px;
            }
        """)
        
        self.choice = "2players"
        self.is_maximized = False
        self.old_pos = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.background_label = QLabel(self)
        self.background_label.setStyleSheet("""
            QLabel {
                border-radius: 15px;
            }
        """)
        
        image_path = resource_path("assets/images/frame1/image.png")
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load background image '{image_path}'")
            self.setStyleSheet("""
                QDialog {
                    background-color: #222222;
                    border-radius: 15px;
                }
            """)
        else:
            print(f"Background image size: {pixmap.width()}x{pixmap.height()}")
            scaled_pixmap = pixmap.scaled(780, 655, Qt.AspectRatioMode.KeepAspectRatio)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.background_label.setGeometry(0, 0, 780, 655)
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("""
                QWidget {
                background-color: #3A393B;
                color: white;
                font-size: 16px;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }""")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(0)
        title_label = QLabel("Game Mode")
        title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
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
        players_image = resource_path("assets/images/frame1/2players.png")
        self.single_button.setStyleSheet("""
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
        """.format(players_image))
        self.single_button.clicked.connect(lambda: self.select_choice("2players"))
        self.multi_button = QPushButton("", self.content_widget)
        self.multi_button.setFixedSize(359, 107)
        self.multi_button.setGeometry(375, 380, 359, 107)
        playerVs_image= resource_path("assets/images/frame1/playerVS.png")
        self.multi_button.setStyleSheet("""
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
        """.format(playerVs_image))
        self.multi_button.clicked.connect(lambda: self.select_choice("player&AI"))
        self.content_layout.addStretch()
        self.title_bar.raise_()
        self.content_widget.raise_()

    def select_choice(self, choice):
        self.choice = choice
        self.accept()

    def get_choice(self):
        return self.choice
    
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

    
