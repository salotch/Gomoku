from Board import GomokuBoard, Board
from GameEngine import GameEngine
from Player import Player, HumanPlayer , AIMinimaxPlayer

# player = HumanPlayer('o', 'maro')
#
# player.get_next_move()
#
# print(player.symbol)


game = GameEngine(HumanPlayer('X', 'Maro'), AIMinimaxPlayer("O","AI"), GomokuBoard())
game.play()

