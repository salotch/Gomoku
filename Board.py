from abc import ABC, abstractmethod


class Board(ABC):
    def __init__(self, num_rows=5, num_columns=5):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board = [['.' for _ in range(num_columns)] for _ in range(num_rows)]
        self.n_moves = 0

    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def update_board(self, x, y, symbol):
        pass

    @abstractmethod
    def is_winner(self, symbol):
        pass

    @abstractmethod
    def is_winner_horizontally(self, symbol):
        pass

    @abstractmethod
    def is_winner_vertically(self, symbol):
        pass

    @abstractmethod
    def is_winner_right_diagonal(self, symbol):
        pass

    @abstractmethod
    def is_winner_left_diagonal(self, symbol):
        pass

    @abstractmethod
    def is_draw(self):
        pass
     
    @abstractmethod
    def reset_board(self):
        pass

class GomokuBoard(Board):

    def display_board(self):
        print()
        for i in range(self.num_rows):
            print("|", end="")
            for j in range(self.num_columns):
                if (self.board[i][j] == '.'):
                    x_digits = 3 - len(str(i))
                    y_digits = 3 - len(str(j))
                    print(x_digits * " ", f"({i},{j})", y_digits * " ", end="|")
                else:
                    print(f"     {self.board[i][j]}     |", end="")
                # print(f"({i},{j}) {self.board[i][j]:>2} |")
            print("\n", "-" * 12 * self.num_columns)
        print()

    def update_board(self, x, y, symbol):
        if x >= 0 and y >= 0 and x < self.num_rows and y < self.num_columns and self.board[x][y] == '.':
            self.board[x][y] = symbol
            self.n_moves += 1
            return True
        print("can't add in this place choose another one")
        return False

    def is_winner(self, symbol):
        if(self.n_moves < 9):
            return False
        return (self.is_winner_left_diagonal(symbol) or
                self.is_winner_right_diagonal(symbol) or
                self.is_winner_horizontally(symbol) or
                self.is_winner_vertically(symbol))


    def is_winner_horizontally(self, symbol):
        for i in range(0, self.num_rows):
            for j in range(2, self.num_columns - 2):
                if (self.board[i][j] == symbol and
                        self.board[i][j - 1] == symbol and
                        self.board[i][j - 2] == symbol and
                        self.board[i][j + 1] == symbol and
                        self.board[i][j + 2] == symbol):
                    return True
        return False


    def is_winner_vertically(self, symbol):
        for i in range(2, self.num_rows - 2):
            for j in range(0, self.num_columns):
                if (self.board[i][j] == symbol and
                        self.board[i - 1][j] == symbol and
                        self.board[i - 2][j] == symbol and
                        self.board[i + 1][j] == symbol and
                        self.board[i + 2][j] == symbol):
                    return True
        return False


    def is_winner_right_diagonal(self, symbol):
        for i in range(2, self.num_rows - 2):
            for j in range(self.num_columns - 3, 1, -1):
                if (self.board[i][j] == symbol and
                        self.board[i - 1][j + 1] == symbol and
                        self.board[i - 2][j + 2] == symbol and
                        self.board[i + 1][j - 1] == symbol and
                        self.board[i + 2][j - 2] == symbol):
                    return True
        return False


    def is_winner_left_diagonal(self, symbol):
        for i in range(2, self.num_rows - 2):
            for j in range(2, self.num_columns - 2):
                if (self.board[i][j] == symbol and
                        self.board[i - 1][j - 1] == symbol and
                        self.board[i - 2][j - 2] == symbol and
                        self.board[i + 1][j + 1] == symbol and
                        self.board[i + 2][j + 2] == symbol):
                    return True
        return False


    def is_draw(self):
        return self.n_moves >= self.num_rows * self.num_columns
    
    def display_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def reset_board(self):
        print("Resetting board")
        self.board = [['.' for _ in range(self.num_columns)] for _ in range(self.num_rows)]
        self.n_moves = 0