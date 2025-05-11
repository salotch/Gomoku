from Board import GomokuBoard, Board
from Player import Player, AIMinimaxPlayer


class GameEngine:
    def __init__(self, player1: Player, player2: Player, board: Board):
        self.player1 = player1
        self.player2 = player2
        self.board = board

    def play(self):
        current_player = self.player1
        self.board.display_board()
        while(self.board.is_draw() == False):

            if(isinstance(current_player,AIMinimaxPlayer)):
                current_player.board=self.board
            x, y = current_player.get_next_move()
            while(self.board.update_board(x, y, current_player.symbol) == False):
                x, y = current_player.get_next_move()

            self.board.display_board()
            if self.board.is_winner(current_player.symbol):
                print(f"{current_player.name} is the winner congrats! 🥳")
                return
            if(self.board.is_draw()):
                print(f"there is a draw between {self.player1.name} and {self.player2.name} play again!")

            if (current_player == self.player1):
                current_player = self.player2
            else:
                current_player = self.player1
