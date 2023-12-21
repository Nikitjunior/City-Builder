import pygame
import sys
import os
class Cell:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y


class Building(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.income = 100

    def build(self):
        pass    # создать объект классa Building на координатах x, y


class Field(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.price = 100
        self.bougt = False

    def buy(self):
        self.bougt = True
        pass

    def build(self):
        pass


class Board():
    def __init__(self, width: int, height: int, screen):
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]
        self.screen = screen
        boardfield = pygame.image.load('data_images/fon-trava.jpg') # фон
        screen.blit(boardfield, (0, 0))
        self.render()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        print(x // 50, y // 50)

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (50 * j, 50 * i,
                                                   50, 50), 1)



if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    board = Board(20, 14, screen)
    field = Field(0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.is_clicked(event.pos)
    pygame.quit()
