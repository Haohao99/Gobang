import pygame
import os

black = pygame.image.load(os.path.join("img", "black_piece.png"))
white = pygame.image.load(os.path.join("img", "white_piece.png"))
class Gobang():
    boardSize = (80, 80, 510, 510)
    initialX = boardSize[0]
    initialY = boardSize[1]
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
    def draw(self, screen):
        if self.color == "w":
            drawThis = pygame.transform.scale(black, (46, 46))
        else:
            drawThis = pygame.transform.scale(white, (46, 46))
        i = (4 - self.col) + round(self.initialX + (self.col * self.boardSize[2] / 11))
        j = 3 + round(self.initialY + (self.row * self.boardSize[3] / 11))
        screen.blit(drawThis, (i, j))

