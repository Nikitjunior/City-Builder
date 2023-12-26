import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data_images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Road(pygame.sprite.Sprite):
    image = load_image("roads.png")

    def __init__(self, group: pygame.sprite.Group, x: int, y: int):
        super().__init__(group)
        self.x, self.y = x, y

        self.image = Road.image.subsurface((250, 0, 250, 250))
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)
        group.update()

    def update(self):
        self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)

        neighbours = [(self.x, y) for y in range(self.y - 1, self.y + 2) if
                      (y != self.y and 0 <= y <= board.height - 1 and isinstance(board.board[y][self.x], Road))]
        neighbours += [(x, self.y) for x in range(self.x - 1, self.x + 2) if
                       (x != self.x and 0 <= x <= board.width - 1 and isinstance(board.board[self.y][x], Road))]

        if 0 == len(neighbours) or len(neighbours) >= 3:
            self.image = Road.image.subsurface((250, 0, 250, 250))
        elif len(neighbours) == 1:
            x, y = neighbours[0]
            if y > self.y or y < self.y:
                self.image = Road.image.subsurface((0, 0, 250, 250))
            elif x > self.x or x < self.x:
                self.image = Road.image.subsurface((0, 0, 250, 250))
                self.image = pygame.transform.rotate(self.image, 90)
        elif len(neighbours) == 2:
            t1, t2 = neighbours
            x1, y1 = t1
            x2, y2 = t2
            if (x1 < self.x < x2) or (x2 < self.x < x1):
                self.image = Road.image.subsurface((0, 0, 250, 250))
                self.image = pygame.transform.rotate(self.image, 90)
            elif (y1 < self.y < y2) or (y2 < self.y < y1):
                self.image = Road.image.subsurface((0, 0, 250, 250))
            elif ((x1 > self.x and self.y == y1) and (y2 > self.y and x2 == self.x)) or (
                    (x2 > self.x and self.y == y2) and (y1 > self.y and x1 == self.x)):
                self.image = Road.image.subsurface((500, 0, 250, 250))
                self.image = pygame.transform.rotate(self.image, 270)
            elif ((x1 > self.x and self.y == y1) and (y2 < self.y and x2 == self.x)) or (
                    (x2 > self.x and self.y == y2) and (y1 < self.y and x1 == self.x)):
                self.image = Road.image.subsurface((500, 0, 250, 250))
            elif ((x1 < self.x and self.y == y1) and (y2 < self.y and x2 == self.x)) or (
                    (x2 < self.x and self.y == y2) and (y1 < self.y and x1 == self.x)):
                self.image = Road.image.subsurface((500, 0, 250, 250))
                self.image = pygame.transform.rotate(self.image, 90)
            elif ((x1 < self.x and self.y == y1) and (y2 > self.y and x2 == self.x)) or (
                    (x2 < self.x and self.y == y2) and (y1 > self.y and x1 == self.x)):
                self.image = Road.image.subsurface((500, 0, 250, 250))
                self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)


class Button(pygame.sprite.Sprite):
    image = load_image("button.png")

    def __init__(self, group: pygame.sprite.Group, screen, x: int, y: int, width: int, height: int):
        super().__init__(group)
        self.screen = screen
        self.x, self.y, self.width, self.height = x, y, width, height

        self.image = Button.image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def update(self):
        x1, y1 = pygame.mouse.get_pos()
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            print("click")

    def set_image(self, image):
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


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

    def build(self):
        pass  # создать объект классa Building на координатах x, y


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
    def __init__(self, width: int, height: int, screen):
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]
        self.screen = screen
        boardfield = pygame.image.load('data_images/fon-trava.jpg')  # фон
        screen.blit(boardfield, (0, 0))
        self.render()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        return (x // CELL_SIZE, y // CELL_SIZE)

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (CELL_SIZE * j, CELL_SIZE * i,
                                                   CELL_SIZE, CELL_SIZE), 1)


if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1000, 700
    CELL_SIZE = 25
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    board = Board(40, 28, screen)
    roads = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = board.is_clicked(event.pos)
                    board.board[y][x] = Road(roads, x, y)
                    roads.draw(screen)
                    roads.update()
        pygame.display.flip()
    pygame.quit()
