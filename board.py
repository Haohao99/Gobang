from piece import Gobang
import time

class Board:
    boardSize = (113, 113, 525, 525)
    initialX = boardSize[0]
    initialY = boardSize[1]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.start_user = 'b'
        self.ready = False
        self.last = None
        self.copy = True
        self.board = [[0 for x in range(11)] for _ in range(rows)]
        self.player1 = "Player 1"
        self.plater2 = "Player 2"
        self.turn = "b"
        self.time1 = 900
        self.time2 = 900
        self.storedTime1 = 0
        self.storedTime2 = 0
        self.winner = None
        self.startTime = time.time()

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)

    def select(self, col, row, color):

        # if piece
        if self.board[row][col] != 0 and self.board[row][col].color != color:
            changed = False

        else:
            self.board[row][col] = Gobang(row, col, color)
            changed = True
        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset_selected()
            else:
                self.turn = "w"
                self.reset_selected()

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        for i in range(self.rows):
            current = 0
            for j in range(self.cols):
                if (self.board[i][j] == 0):
                    current = 0
                if(type(self.board[i][j]) is not int):
                    if (self.board[i][j].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        for i in range(self.cols):
            current = 0
            for j in range(self.rows):
                if (self.board[j][i] == 0):
                    current = 0
                if (type(self.board[j][i]) is not int):
                    if (self.board[j][i].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        # top left to top right left half
        for i in range(0, self.rows - 4):
            row = i
            col = 0
            current = 0
            for j in range(self.cols):
                row += 1
                col += 1
                if (row > self.rows - 1 or col > self.cols - 1):
                    break
                if (self.board[row][col] == 0):
                    current = 0
                if (type(self.board[row][col]) is not int):
                    if (self.board[row][col].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        # top left to top right right half
        for i in range(0, self.cols - 4):
            row = 0
            col = i
            current = 0
            for j in range(self.rows):
                row += 1
                col += 1
                if (row > self.rows - 1 or col > self.cols - 1):
                    break
                if (self.board[row][col] == 0):
                    current = 0
                if (type(self.board[row][col]) is not int):
                    if (self.board[row][col].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        # bottom left to top right lower half
        for i in range(0, self.cols - 4):
            row = self.cols - 1
            col = i
            current = 0
            for j in range(self.rows):
                row -= 1
                col += 1
                if (row < 0 or col > self.cols-1):
                    break
                if (self.board[row][col] == 0):
                    current = 0
                if (type(self.board[row][col]) is not int):
                    if (self.board[row][col].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        # bottom left to top right upper half
        for i in range(0, self.cols - 4):
            row = self.cols - 1 - i
            col = 0
            current = 0
            for j in range(self.rows):
                row -= 1
                col += 1
                if (row < 0 or col > self.rows - 1):
                    break
                if (self.board[row][col] == 0):
                    current = 0
                if (type(self.board[row][col]) is not int):
                    if (self.board[row][col].color == color):
                        current += 1
                    else:
                        current = 0
                    if (current == 5):
                        return True
        return False




