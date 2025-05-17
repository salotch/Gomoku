from Board import GomokuBoard, Board
from Player import AIAlphaBetaPruningPlayer, Player, AIMinimaxPlayer
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer
from ChooseMode import Winner

class GameEngine:
    def __init__(self, player1: Player, player2: Player, board: Board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.current_player = player1
        self.game_over = False
        self.timer = None
        self.game_board = board

    def play(self):
        self.current_player = self.player1
        self.board.display_board()
        while not self.board.is_draw() and not self.game_over:
            if isinstance(self.current_player, (AIMinimaxPlayer, AIAlphaBetaPruningPlayer)):
                self.current_player.board = self.board
            x, y = self.current_player.get_next_move()
            while not self.board.update_board(x, y, self.current_player.symbol):
                x, y = self.current_player.get_next_move()
            self.board.display_board()
            if self.board.is_winner(self.current_player.symbol):
                print(f"{self.current_player.name} is the winner congrats! 🥳")
                self.game_over = True
                return
            if self.board.is_draw():
                print(f"There is a draw between {self.player1.name} and {self.player2.name}, play again!")
                self.game_over = True
                return
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def playMoodGUI(self, mode, game_board):
        self.current_player = self.player1
        self.game_board = game_board
        self.mode = mode
        self.game_board.set_engine(self)
        if mode == "aiVSAI":
            # self.game_board.disable_board()
            self.process_ai_move()
        elif mode == "player&AI" and isinstance(self.player2, (AIMinimaxPlayer, AIAlphaBetaPruningPlayer)):
            self.player2.board = self.board

    def process_move(self, row, col, button):
        if self.mode == "2players" or (self.mode == "player&AI" and self.current_player == self.player1):
            if self.board.update_board(row, col, self.current_player.symbol):
                button.setIcon(self.game_board.black_stone_icon if self.current_player.symbol == 'X' else self.game_board.red_stone_icon)
                button.setIconSize(self.game_board.icon_size)
                
                if self.check_game_state():
                    return
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                if self.mode == "player&AI" and isinstance(self.current_player, (AIMinimaxPlayer, AIAlphaBetaPruningPlayer)):
                    self.timer = QTimer()
                    self.timer.setSingleShot(True)
                    self.timer.timeout.connect(self.process_ai_move)
                    self.timer.start(1000)
            else:
                QMessageBox.warning(self.game_board, "Invalid Move", "This position is already taken. Choose another.")

    def process_ai_move(self):
        if self.game_over:
            return
        
        self.current_player.board = self.board
        try:
            x, y = self.current_player.get_next_move()
            while not self.board.update_board(x, y, self.current_player.symbol):
                x, y = self.current_player.get_next_move()
            button = self.game_board.buttons[(x, y)]
            button.setIcon(self.game_board.black_stone_icon if self.current_player.symbol == 'X' else self.game_board.red_stone_icon)
            button.setIconSize(self.game_board.icon_size)
           
            if self.check_game_state():
                return
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            if self.mode == "aiVSAI" and not self.game_over:
                self.timer = QTimer()
                self.timer.setSingleShot(True)
                self.timer.timeout.connect(self.process_ai_move)
                self.timer.start(1000)
        except Exception as e:
            QMessageBox.critical(self.game_board, "Error", f"AI move failed: {str(e)}")
            self.game_over = True
            self.game_board.disable_board()

    def check_game_state(self):
        if self.board.is_winner(self.current_player.symbol):
            winner = "player1" if self.current_player.symbol=="X" else "player2"
            dialog = Winner(self.game_board,winner =winner)
            if dialog.exec():
                choice = dialog.get_choice()
                if choice == "playAgain":
                    self.game_over = False
                    self.board.reset_board()
                    self.current_player = self.player1
                    self.game_board.enable_board()
                    if self.mode == "aiVSAI":
                        self.process_ai_move()
                    return False
                else:  # exit
                    self.game_over = True
                    self.game_board.disable_board()
                    if self.timer:
                        self.timer.stop()
                return True
        if self.board.is_draw():
            winner = "Draw"
            dialog = Winner(self.game_board,winner=winner)
            if dialog.exec():
                choice = dialog.get_choice()
                if choice == "playAgain":
                    self.game_over = False
                    self.board.reset_board()
                    self.current_player = self.player1
                    self.game_board.enable_board()
                    return False
                else:  # exit
                    self.game_over = True
                    self.game_board.disable_board()
                    if self.timer:
                        self.timer.stop()
                    return True
        return False
