import pygame


class Cell:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def is_clicked(self, pos: tuple):
        x, y = pos
        pass  # to do click react!


class Building(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.income = 100

    def upgrade(self):
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


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]


if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    board = Board(5, 5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
