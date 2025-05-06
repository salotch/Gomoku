from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, symbol, name=None):
        self.x = None
        self.y = None
        self.symbol = symbol
        self.name = name

    @abstractmethod
    def get_next_move(self):
        pass


class HumanPlayer(Player):
    def get_next_move(self):
        next_move = input(f'Enter your next move {self.name}: ')
        self.x, self.y = map(int, next_move.strip().split())
        return self.x, self.y


class AIMinimaxPlayer(Player):
    def get_next_move(self):
        # add your logic here to get x and y using AI Minimax algorithm
        pass


class AIAlphaBetaPruningPlayer(Player):
    def get_next_move(self):
        # add your logic here to get x and y using AI Alpha-Beta Pruning algorithm
        pass
