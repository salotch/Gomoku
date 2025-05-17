from Board import GomokuBoard, Board
from GameEngine import GameEngine
from Player import AIAlphaBetaPruningPlayer, Player, HumanPlayer , AIMinimaxPlayer

# player = HumanPlayer('o', 'maro')
#
# player.get_next_move()
#
# print(player.symbol)


game = GameEngine(HumanPlayer('X', 'Maro'), AIAlphaBetaPruningPlayer("O","AI"), GomokuBoard(15,15))
game.play()
