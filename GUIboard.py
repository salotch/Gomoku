from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize



class GameBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cell_size = 40
        self.grid_size = 15
        self.black_stone_icon = QIcon("assets/images/frame2/bStone.png")
        self.red_stone_icon = QIcon("assets/images/frame2/rStone.png")
        self.icon_size = QSize(self.cell_size, self.cell_size)
        self.offset_x = 77
        self.offset_y = 52
        self.setFixedSize(1300, 800)
        self.buttons = {}
        self.engine = None
        print("Class initiated")
        self.init_board()

    def set_engine(self, engine):
        self.engine = engine

    def init_board(self):
        print("Board initiated")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
                if col > 0:
                    x += 7 * col
                if row > 0:
                    y += 7 * row
                btn = QPushButton(self)
                btn.setGeometry(x, y, self.cell_size, self.cell_size)
                btn.setStyleSheet("background-color: transparent; border: none;")
                btn.setProperty("row", row)
                btn.setProperty("col", col)
                self.buttons[(row, col)] = btn
                btn.clicked.connect(self.make_click_handler(btn, row, col))

    def make_click_handler(self, button, row, col):
        def handler():
            print(f"Clicked on ({row}, {col})")
            if self.engine is None:
                return
            self.engine.process_move(row, col, button)
        return handler
            
    def disable_board(self):
        print("Disabling board")
        for btn in self.buttons.values():
            btn.setEnabled(False)
            btn.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: none;")

    def enable_board(self):
        print("Enabling board")
        for btn in self.buttons.values():
            btn.setEnabled(True)
            btn.setIcon(QIcon())  # Clear icons
            btn.setStyleSheet("background-color: transparent; border: none;")