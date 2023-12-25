import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


#class Button(pygame.sprite.Sprite):
    #image = load_image("button.png")

    #def __init__(self, group, screen, x: int, y: int, width: int, height: int):
        #super().__init__(group)
        #self.screen = screen
        #self.x, self.y, self.width, self.height = x, y, width, height

        #self.image = Button.image
        #self.image = pygame.transform.scale(self.image, (width, height))
        #self.rect = self.image.get_rect()
        #self.rect = self.rect.move(self.x, self.y)

    #def update(self):
        #x1, y1 = pygame.mouse.get_pos()
        #if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            #print("click")

    #def set_image(self, image):
        #self.image = load_image(image)
        #self.image = pygame.transform.scale(self.image, (self.width, self.height))


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
        self.coins = 1000
        self.banknotes = 50
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]
        self.screen = screen
        boardfield = load_image('fon-trava.jpg')
        screen.blit(boardfield, (0, 0))
        self.render()
        self.hood()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        print(x // 50, y // 50)

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (50 * j, 50 * i,
                                                   50, 50), 1)
    def hood(self):
        pygame.draw.rect(screen, 'white', (0, 0, 200, 50))
        coinimage = load_image('coin.jpg')
        screen.blit(coinimage, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.coins), True, (255, 217, 25))
        screen.blit(text, (50, 25))
        banknoteimage = load_image('banknote.jpg')
        screen.blit(banknoteimage, (110, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.banknotes), True, (84, 255, 159))
        screen.blit(text, (160, 25))
        #self.shop = Button(???)
        #self.destruct = Button(???) Обговорим как работает класс Button




if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
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
