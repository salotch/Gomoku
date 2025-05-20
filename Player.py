from abc import ABC, abstractmethod
import copy


class Player(ABC):
    def __init__(self, symbol, name="Maro"):
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
    def __init__(self, symbol, name=None, depth=2):
        super().__init__(symbol, name)
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.board= None
        self.max_depth = depth  
##################################################################################
# this is how u know it was me who commented here --> :DDDDDDD
    def get_next_move(self):  # Poly :DDDD
        best_score = float('-inf')
        best_move = None
        for x in range(self.board.num_rows):
            for y in range(self.board.num_columns):
              if self.board.board[x][y] == '.' :
                    tmp = copy.deepcopy(self.board) ## 34AN NA5OD KOL EL ATTRIBUTES :D
                    tmp.update_board(x, y, self.symbol)
                    score = self.minimax(tmp, False, 1)

                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move
#######################################################################################
    def minimax(self, board, is_maximizing, depth):
        if board.is_winner(self.symbol):
            return 2 # Ai
        if board.is_winner(self.opponent_symbol):
            return -2 # User
        if board.is_draw() or depth == self.max_depth:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for x in range(board.num_rows):
             for y in range(board.num_columns):
              if board.board[x][y] == '.' : ## empty ?
                tmp = copy.deepcopy(board)## 34an n copy kol al attributes ely gwa :D man I miss OOP
                tmp.update_board(x, y, self.symbol) # grb t update kda ? :D
                score = self.minimax(tmp, False, depth + 1)  # W 4oof :D
                # since its a tmp variable we dont really care about it , no point to undo in it
                best_score = max(best_score, score) 
            return best_score
        else:
            best_score = float('inf')
            for x in range(board.num_rows):
             for y in range(board.num_columns):
              if board.board[x][y] == '.' :
                tmp = copy.deepcopy(board)
                tmp.update_board(x, y, self.opponent_symbol)
                score = self.minimax(tmp, True, depth + 1)
                best_score = min(best_score, score)
            return best_score
#############################################################################################################
class AIAlphaBetaPruningPlayer(Player):
    def __init__(self, symbol, name=None, depth=2):
        super().__init__(symbol, name)
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.board= None
        self.max_depth = depth  
    def get_next_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for x in range(self.board.num_rows):
           for y in range(self.board.num_columns):
              if self.board.board[x][y] == '.' :
                 tmp = copy.deepcopy(self.board)
                 tmp.update_board(x, y, self.symbol)
                 score = self.alpha_beta(tmp, False, 1, alpha, beta)
                 if score > best_score:
                    best_score = score
                    best_move = (x, y)
                 alpha = max(alpha, score) #3ashan alpha bta3at al root
        return best_move
    #############################################################################################################
    def alpha_beta(self, board, is_maximizing, depth, alpha, beta):
        if board.is_winner(self.symbol):
            return 2 # Ai
        if board.is_winner(self.opponent_symbol):
            return -2 # User
        if board.is_draw() or depth == self.max_depth:
            return 0
        if is_maximizing:
           best_score = float('-inf')
           for x in range(board.num_rows):
              for y in range(board.num_columns):
                 if board.board[x][y] == '.' :
                    tmp = copy.deepcopy(board)
                    tmp.update_board(x, y, self.symbol)
                    score = self.alpha_beta(tmp, False, depth + 1, alpha, beta)
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if alpha >= beta: #hna hashof al condation lw tmm h3aml cutoff
                       break
              if alpha >= beta: #hna ha3mal break the outer loop
                 break
          
           return best_score
        else:
           best_score = float('inf')
           for x in range(board.num_rows):
              for y in range(board.num_columns):
                 if board.board[x][y] == '.' :
                    tmp = copy.deepcopy(board)
                    tmp.update_board(x, y, self.opponent_symbol)
                    score = self.alpha_beta(tmp, True, depth + 1, alpha, beta)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if alpha >= beta: #hna hashof al condation lw tmm h3aml cutoff
                       break
              if alpha >= beta: #hna ha3mal break the outer loop
                 break
                 
           return best_score