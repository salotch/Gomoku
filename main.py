from Board import GomokuBoard, Board
from GameEngine import GameEngine
from Player import Player, HumanPlayer

# player = HumanPlayer('o', 'maro')
#
# player.get_next_move()
#
# print(player.symbol)


game = GameEngine(HumanPlayer('X', 'Maro'), HumanPlayer('O', 'Sara'), GomokuBoard())
game.play()

