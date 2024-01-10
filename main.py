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


class Button(pygame.sprite.Sprite):
    # 3image = load_image("button.png")

    def __init__(self, group, screen, x: int, y: int, width: int, height: int):
        super().__init__(group)
        self.screen = screen
        self.x, self.y, self.width, self.height = x, y, width, height

        # self.image = Button.image
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
    def __init__(self, width: int, height: int, screen, top: int, right: int):
        # на поле(напр. на поле  и на магазин одновременно
        self.top = top
        self.right = right
        self.coins = 100
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]
        self.screen = screen
        boardfield = load_image('fon-trava.jpg')
        screen.blit(boardfield, (0, 50))
        self.render()
        self.hood()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        print(x // 50, (y - self.top) // 50)

    # todo вместо этого сделать по нажатию вывод инфы о здании, дороге итп.

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (50 * j, 50 * i + self.top,
                                                   50, 50), 1)

    def hood(self):
        pygame.draw.rect(screen, 'white', (0, 0, 200, 50))
        coinimage = load_image('coin.jpg')
        screen.blit(coinimage, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.coins), True, (255, 217, 25))
        screen.blit(text, (50, 25))

    def updatemoney(self):
        pass  # todo обновление кол-ва монет при их изменении


class Shop():
    def __init__(self, screen, x: int, y: int, hw: int, image):
        self.opened = False
        self.buildingsdict = {'Дома': [], 'Комм.службы': [], 'Коммерция': []}
        self.screen = screen
        self.x = x
        self.y = y
        self.hw = hw
        self.shopimage = load_image(image)
        pygame.draw.rect(screen, (8, 204, 78), (self.x, self.y, self.hw + 1, self.hw),
                         0)  # todo сделать чтобы при наведении на неё кнопка реагировала(меняла цвет)
        self.shopimage = pygame.transform.scale(self.shopimage, (hw, hw))
        screen.blit(self.shopimage, (1000, 50))
        pygame.display.flip()

    def startshop(self):
        self.opened = True
        self.copyscreen = screen
        pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                   800, 500), 0)
        self.type = 'дома'  # изначально открывается вкладка с домами
        self.openshop()
        housemenuim = pygame.transform.scale(load_image('house1.png'), (50, 50))
        electromenuim = pygame.transform.scale(load_image('electro.png'), (50, 50))
        othersmenuim = pygame.transform.scale(load_image('hospital.png'), (50, 50))
        screen.blit(housemenuim, (850, 150))
        screen.blit(electromenuim, (850, 200))
        screen.blit(othersmenuim, (850, 250))
        pygame.display.flip()

    def openshop(self):  # todo сделать реакцию на наведение в магазине
        if self.type == 'дома':
            self.drawbuildinginshop(0, 0, 'Частный домик', 'Прибыль: 10 (30сек.) Население: +8',
                                    'Требуемая электроэнергия: 1', '40',pygame.transform.scale(load_image('house1.png'),
                                                                                          (130, 130)))
            self.drawbuildinginshop(1, 0, 'Двухэтажный дом', 'Прибыль: 30 (1 мин.) Население: +20',
                                    'Требуемая электроэнергия: 2', '100', pygame.transform.scale(load_image('house2.jpg'),
                                                                                          (130, 120)))
            self.drawbuildinginshop(2, 0, 'Многоквартирный дом', 'Прибыль: 100 (2 мин.) Население: +40',
                                    'Требуемая электроэнергия: 3', '250', pygame.transform.scale(load_image('house3.png'),
                                                                                          (130, 130)))
        if self.type == 'коммуналка':
            pass

        if self.type == 'службы':
            pass

    def drawbuildinginshop(self, row, col, name, par1, par2, cost, image):
        font1 = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 15)
        font3 = pygame.font.Font(None, 25)
        text = font1.render(name, True, (6, 128, 47))
        text2 = font2.render(par1, True, (0, 0, 0))
        text3 = font2.render(par2, True, (0, 0, 0))
        text4 = font3.render(cost, True, (255, 217, 25))
        screen.blit(image, (130 + 255 * row, 180 + 250 * col))
        screen.blit(pygame.transform.scale(load_image('coin.jpg'), (40, 40)), (170 + 250 * row, 340 + 250 * col))
        screen.blit(text, (125 + 240 * row, 155 + 250 * col))
        screen.blit(text2, (125 + 245 * row, 310 + 250 * col))
        screen.blit(text3, (135 + 245 * row, 320 + 250 * col))
        screen.blit(text4, (210 + 250 * row, 355 + 250 * col))
        pygame.display.flip()

    def shopclickreact(self, pos):
        if 550 <= pos[0] <= 600 and 150 <= pos[1] <= 200:
            self.type = 'дома'
            self.openshop()
        if 550 <= pos[0] <= 600 and 200 <= pos[1] <= 250:
            self.type = 'коммуналка'
            self.openshop()
        if 550 <= pos[0] <= 600 and 250 <= pos[1] <= 300:
            self.type = 'службы'
            self.openshop()


if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1100, 750
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    board = Board(20, 14, screen, 50, 100)
    field = Field(0, 0)
    shop = Shop(screen, 999, 50, 100, 'shop.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not shop.opened:
                    if 1000 <= event.pos[0] <= 1100 and 50 <= event.pos[1] <= 150:
                        shop.startshop()
                    if 0 <= event.pos[0] <= 1000 and 50 <= event.pos[1] <= 750:
                        board.is_clicked(event.pos)
                else:
                    shop.shopclickreact(event.pos)

    pygame.quit()
