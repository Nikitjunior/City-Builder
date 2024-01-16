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


class Button(pygame.sprite.Sprite):
    image = load_image("button.png")

    def __init__(self, group, screen, x: int, y: int, width: int, height: int):
        super().__init__(group)
        self.screen = screen
        self.x, self.y, self.width, self.height = x, y, width, height

        self.image = Button.image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def update(self):
        try:
            x1, y1 = pygame.mouse.get_pos()
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                self.funk()
        except AttributeError:
            print("У кнопки нет функции.")

    def set_image(self, image):
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def connect(self, funk):
        self.funk = funk


class Building(pygame.sprite.Sprite):
    image = load_image("house1.png")

    def __init__(self, group, x: int, y: int):
        super().__init__(group)
        self.x, self.y = x, y
        self.lvl = 0
        self.income = 1
        self.image = Building.image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)

    def __repr__(self):
        return "B"

    def bring_income(self):
        global balance
        ipf = self.income / FPS     # Income Per Frame
        balance += ipf

    def set_image(self, path: str):
        self.image = load_image(path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def level_up(self):
        pass

    def update(self):
        if self.image:
            self.bring_income()
            self.rect.move(self.x / CELL_SIZE, self.y / CELL_SIZE)
        else:
            raise NoImageError


class Field:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return 'F'


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

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def __str__(self):
        value = ""
        for i in self.board:
            value += f"{i}" + "\n"
        return value

    def click_pos(self):
        x, y = pygame.mouse.get_pos()
        return x // CELL_SIZE, y // CELL_SIZE

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (CELL_SIZE * j, CELL_SIZE * i,
                                                   CELL_SIZE, CELL_SIZE), 1)


if __name__ == '__main__':
    balance = 0
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1100, 750
    CELL_SIZE = 50
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    board = Board(1000 // CELL_SIZE, 700 // CELL_SIZE, screen)

    clock = pygame.time.Clock()
    FPS = 60

    buildings = pygame.sprite.Group()
    building = Building(buildings, 0, 0)
    board[0][0] = building
    building.set_image("house2.png")
    buildings.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = board.click_pos()
                    if isinstance(board[y][x], Field):
                        board[y][x] = Building(buildings, x, y)
                        buildings.draw(screen)
        buildings.update()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
