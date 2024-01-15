import pygame
import os
import sys

CELL_SIZE = 50


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

    def update_texture(self):

        neighbours = [(self.x, y) for y in range(self.y - 1, self.y + 2) if
                      (y != self.y and 0 <= y <= board.height - 1 and isinstance(board.board[y][self.x], Road))]
        neighbours += [(x, self.y) for x in range(self.x - 1, self.x + 2) if
                       (x != self.x and 0 <= x <= board.width - 1 and isinstance(board.board[self.y][x], Road))]

        if 0 == len(neighbours) or len(neighbours) > 3:
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
        elif len(neighbours) == 3:
            self.image = self.image = Road.image.subsurface((750, 0, 250, 250))
            for t1 in neighbours:
                for t2 in neighbours:
                    for t3 in neighbours:
                        if t1 != t2 != t3:
                            x1, y1 = t1
                            x2, y2 = t2
                            x3, y3 = t3
                            if ((x1 > self.x > x2) and self.x == x3) and ((y1 == self.y == y2) and self.y > y3):
                                self.image = pygame.transform.rotate(self.image, 90)
                            elif ((x1 > self.x > x2) and self.x == x3) and ((y1 == self.y == y2) and self.y < y3):
                                self.image = pygame.transform.rotate(self.image, 270)
                            elif ((x1 == self.x == x2) and x3 > self.x) and ((y1 < self.y < y2) and self.y == y3):
                                pass
                            elif ((x1 == self.x == x2) and x3 < self.x) and ((y1 < self.y < y2) and self.y == y3):
                                self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)

    def update(self):
        self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE)
        self.update_texture()


class Button(pygame.sprite.Sprite):
    # image = load_image("button.png")

    def __init__(self, group: pygame.sprite.Group, screen, x: int, y: int, width: int, height: int):
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


# class Building(Cell):
# def __init__(self, x: int, y: int):
# super().__init__(x, y)
# self.income = 100

# def build(self, x, y, li):
# buildimage = load_image(li[1])
# screen.blit(buildimage, (x * 50, y * 50))


class Board:
    def __init__(self, width: int, height: int, screen, top: int, right: int):
        self.isbuilding = False
        self.top = top
        self.right = right
        self.coins = 100
        self.width = width
        self.height = height
        self.board = [[[y, x, 'nothingbuild'] for x in range(height)] for y in range(width)]
        self.buildlist = ['дом1', 'house1.png', 10, 30, 8, 1, 40], ['дом2', 'house2.png', 30, 60, 20, 2, 110], ['дом3',
                                                                                                                'house3.png',
                                                                                                                100,
                                                                                                                120, 40,
                                                                                                                3,
                                                                                                                250, ], [
                             'ветряк', 'wind.png', 5, 1, 30], ['солнечная панель', 'solar.png', 9, 2, 55], [
                             'электростанция', 'station.png', 16, 3, 100]
        self.screen = screen
        self.render()
        self.hood()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        # return (x // CELL_SIZE, y // CELL_SIZE)
        if self.isbuilding:
            self.build(x // CELL_SIZE, (y - self.top) // CELL_SIZE, shop.nowbuilding)
        else:
            print(self.board[x // CELL_SIZE][(y - self.top) // CELL_SIZE])

    # todo вместо этого сделать по нажатию вывод инфы о здании, дороге итп.

    def render(self):
        boardfield = load_image('fon-trava.jpg')
        screen.blit(boardfield, (0, self.top))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (CELL_SIZE * j, CELL_SIZE * i + self.top,
                                                   CELL_SIZE, CELL_SIZE), 1)
        for j in range(self.height):
            for i in range(self.width):
                if self.board[i][j][2] != 'nothingbuild':
                    buildimage = pygame.transform.scale(load_image(self.board[i][j][2][1]), (CELL_SIZE, CELL_SIZE))
                    screen.blit(buildimage, (i * CELL_SIZE, j * CELL_SIZE + self.top))

    def hood(self):
        pygame.draw.rect(screen, 'white', (0, 0, 200, 50))
        coinimage = load_image('coin.jpg')
        screen.blit(coinimage, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.coins), True, (255, 217, 25))
        screen.blit(text, (50, 25))

    def updatemoney(self):
        pass  # todo обновление кол-ва монет при их изменении

    def build(self, x, y, li):
        buildimage = pygame.transform.scale(load_image(li[1]), (CELL_SIZE, CELL_SIZE))
        screen.blit(buildimage, (x * CELL_SIZE, y * CELL_SIZE + self.top))
        self.isbuilding = False
        pygame.display.flip()
        self.board[x][y][2] = li


class Shop():
    def __init__(self, x: int, y: int, hw: int, image):
        self.opened = False
        # self.buildingsdict = {'Дома': [], 'Комм.службы': [], 'Коммерция': []}
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
        self.nowbuilding = ''
        self.copyscreen = screen.copy()
        pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                   800, 500), 0)
        self.type = 'дома'  # изначально открывается вкладка с домами
        self.openshop()
        housemenuim = pygame.transform.scale(load_image('house1.png'), (50, 50))
        electromenuim = pygame.transform.scale(load_image('electro.png'), (50, 50))
        othersmenuim = pygame.transform.scale(load_image('hospital.png'), (50, 50))
        closeim = pygame.transform.scale(load_image('close.png'), (50, 50))
        screen.blit(closeim, (850, 150))
        screen.blit(housemenuim, (850, 200))
        screen.blit(electromenuim, (850, 250))
        screen.blit(othersmenuim, (850, 300))
        pygame.display.flip()

    def openshop(self):  # todo сделать реакцию на наведение в магазине
        if self.type == 'дома':
            pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                       750, 500), 0)
            self.drawbuildinginshop(0, 0, 'Частный домик', 'Прибыль: 10 (30сек.) Население: +8',
                                    'Требуемая электроэнергия: 1', '40',
                                    pygame.transform.scale(load_image('house1.png'),
                                                           (130, 130)))
            self.drawbuildinginshop(1, 0, 'Двухэтажный дом', 'Прибыль: 30 (1 мин.) Население: +20',
                                    'Требуемая электроэнергия: 2', '110',
                                    pygame.transform.scale(load_image('house2.png'),
                                                           (130, 130)))
            self.drawbuildinginshop(2, 0, 'Многоквартирный дом', 'Прибыль: 100 (2 мин.) Население: +40',
                                    'Требуемая электроэнергия: 3', '250',
                                    pygame.transform.scale(load_image('house3.png'),
                                                           (130, 130)))
            pygame.display.flip()
        if self.type == 'коммуналка':
            pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                       750, 500), 0)
            self.drawbuildinginshop(0, 0, 'Ветряк', 'Приносит электроэнергии: 5', 'Требуемое население: 1', '30',
                                    pygame.transform.scale(load_image('wind.png'), (130, 130)))
            self.drawbuildinginshop(1, 0, 'Солнечная панель', 'Приносит электроэнергии: 9', 'Требуемое население: 2',
                                    '55', pygame.transform.scale(load_image('solar.png'), (130, 130)))
            self.drawbuildinginshop(2, 0, 'Электростанция', 'Приносит электорэнергии: 16', 'Требуемое население: 3',
                                    '100', pygame.transform.scale(load_image('station.png'), (130, 130)))
            pygame.display.flip()

            if self.type == 'службы':
                pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                           750, 500), 0)
                pass

    def drawbuildinginshop(self, row, col, name, par1, par2, cost, image):
        font1 = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 15)
        font3 = pygame.font.Font(None, 25)
        text1 = font1.render(name, True, (6, 128, 47))
        text2 = font2.render(par1, True, (0, 0, 0))
        text3 = font2.render(par2, True, (0, 0, 0))
        text4 = font3.render(cost, True, (255, 217, 25))
        screen.blit(image, (130 + 255 * row, 180 + 250 * col))
        screen.blit(pygame.transform.scale(load_image('coin.jpg'), (40, 40)), (170 + 250 * row, 340 + 250 * col))
        screen.blit(text1, (125 + 240 * row, 155 + 250 * col))
        screen.blit(text2, (125 + 245 * row, 310 + 250 * col))
        screen.blit(text3, (135 + 245 * row, 320 + 250 * col))
        screen.blit(text4, (210 + 250 * row, 355 + 250 * col))

    def shopclickreact(self, pos):
        if 850 <= pos[0] <= 900 and 150 <= pos[1] <= 200:
            self.closeshop()
        if 850 <= pos[0] <= 900 and 200 <= pos[1] <= 250:
            self.type = 'дома'
            self.openshop()
        if 850 <= pos[0] <= 900 and 250 <= pos[1] <= 300:
            self.type = 'коммуналка'
            self.openshop()
        if 850 <= pos[0] <= 900 and 300 <= pos[1] <= 350:
            self.type = 'службы'
            self.openshop()
        if 100 <= pos[0] <= 350 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[0]
            if self.type == 'коммуналка':
                self.nowbuilding = board.buildlist[3]
            self.closeshop()
            board.isbuilding = True
        if 350 < pos[0] < 600 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[1]
            if self.type == 'коммуналка':
                self.nowbuilding = board.buildlist[4]
            self.closeshop()
            board.isbuilding = True
        if 600 <= pos[0] <= 850 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[2]
            if self.type == 'коммуналка':
                self.nowbuilding = board.buildlist[5]
            self.closeshop()
            board.isbuilding = True

    def closeshop(self):
        board.render()
        pygame.display.flip()
        self.opened = False


if __name__ == '__main__':
    balance = 100
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 1100, 750
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    board = Board(1000 // CELL_SIZE, 700 // CELL_SIZE, screen, 50, 100)
    field = Field(0, 0)
    shop = Shop(999, 50, 100, 'shop.png')

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