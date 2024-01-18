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

    def __init__(self, group, x: int, y: int, building_cost: int, start_income: int):
        super().__init__(group)
        self.x, self.y = x, y
        self.lvl = 0
        self.income = start_income
        self.image = Building.image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE + TOP)
        self.building_cost = building_cost
        self.upgrade_cost = building_cost

    def __repr__(self):
        return "B"

    def bring_income(self):
        global balance
        ipf = self.income / FPS  # Income Per Frame
        balance += ipf

    def set_image(self, path: str):
        self.image = load_image(path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def level_up(self):
        if self.lvl < MAX_LEVEL:
            if balance >= self.upgrade_cost:
                self.lvl += 1
                self.income = round(self.income * 1.5)
                upgrade_cost_multiplier = 2
                self.upgrade_cost = round(upgrade_cost_multiplier * self.upgrade_cost)

    def update(self):
        if self.image:
            self.bring_income()
            self.rect.move(self.x / CELL_SIZE, self.y / CELL_SIZE + TOP)
        #else:
            #raise NoImageError


class Field:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return 'F'


class Board:
    def __init__(self, width: int, height: int, screen, top: int, right: int):
        self.mnojitel = 1
        self.population = 0
        self.electricity = 0
        self.ispopulation = 0
        self.iselectricity = 0
        self.isbuilding = False
        self.top = top
        self.right = right
        self.coins = 1000
        self.width = width
        self.height = height
        self.board = [[[y, x, 'nothingbuild'] for x in range(height)] for y in range(width)]
        self.buildlist = [['дом', 'дом1', 'house1.png', 10, 30, 8, 1, 40],
                          ['дом', 'дом2', 'house2.png', 30, 60, 20, 2, 110],
                          ['дом', 'дом3', 'house3.png', 100, 120, 40, 3, 250, ],
                          ['электро', 'ветряк', 'wind.png', 5, 0, 30],
                          ['электро', 'солнечная панель', 'solar.png', 9, 2, 55],
                          ['электро', 'электростанция', 'station.png', 16, 3, 100],
                          ['службы', 'полицейский участок', 'police.png', 0.25, 7, 30, 220],
                          ['службы', 'больница', 'hospital.png', 0.40, 13, 60, 380],
                          ['службы', 'офисное здание', 'office.jpg', 0.55, 22, 100, 650]]
        self.screen = screen
        self.render()
        self.hood()
        pygame.display.flip()

    def is_clicked(self, pos: tuple):
        x, y = pos
        if self.isbuilding:
            self.build(x // CELL_SIZE, (y - self.top) // CELL_SIZE, shop.nowbuilding)
        else:
            print(self.board[x // CELL_SIZE][(y - self.top) // CELL_SIZE])

    # todo вместо этого сделать по нажатию вывод инфы о здании, дороге итп.

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
        boardfield = pygame.transform.scale(load_image('fon-trava.png'), (1000, 700))
        screen.blit(boardfield, (0, self.top))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (CELL_SIZE * j, CELL_SIZE * i + self.top,
                                                   CELL_SIZE, CELL_SIZE), 1)
        for j in range(self.height):
            for i in range(self.width):
                if self.board[i][j][2] != 'nothingbuild':
                    buildimage = pygame.transform.scale(load_image(self.board[i][j][2][2]), (CELL_SIZE, CELL_SIZE))
                    screen.blit(buildimage, (i * CELL_SIZE, j * CELL_SIZE + self.top))

    def hood(self):
        pygame.draw.rect(screen, 'white', (0, 0, 200, 50))
        coinimage = pygame.transform.scale(load_image('coin.png'), (50, 50))
        screen.blit(coinimage, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.coins), True, (255, 217, 25))
        screen.blit(text, (55, 33))
        peopleimage = pygame.transform.scale(load_image('people.png'), (50, 50))
        screen.blit(peopleimage, (150, 0))
        text = font.render(str(f'{self.population} / {self.ispopulation}'), True, (0, 180, 255))
        screen.blit(text, (200, 33))
        electroimage = pygame.transform.scale(load_image('electro.png'), (50, 50))
        screen.blit(electroimage, (300, 0))
        text = font.render(str(f'{self.electricity} / {self.iselectricity}'), True, (250, 150, 0))
        screen.blit(text, (350, 33))

    def updateparameters(self, li):
        self.errormes = ''
        if self.coins - li[-1] < 0:
            self.errormes = 'Не хватает денег для постройки!'
            return False
        if li[0] == 'дом':
            if li[-2] + self.electricity > self.iselectricity:
                self.errormes = 'Не хватает электроэнергии для постройки!'
                return False
            pygame.draw.rect(screen, 'white', (200, 33, 100, 18), 0)
            pygame.draw.rect(screen, 'white', (350, 33, 100, 18), 0)
            pygame.display.flip()
            self.coins -= li[-1]
            self.electricity += li[-2]
            self.ispopulation += li[5]
            self.hood()
        if li[0] == 'электро':
            if li[-2] + self.population > self.ispopulation:
                self.errormes = 'Не хватает населения для постройки!'
                return False
            pygame.draw.rect(screen, 'white', (200, 33, 100, 18), 0)
            pygame.draw.rect(screen, 'white', (350, 33, 100, 18), 0)
            pygame.display.flip()
            self.coins -= li[-1]
            self.iselectricity += li[3]
            self.population += li[4]
            self.hood()
        if li[0] == 'службы':
            if li[-2] + self.population > self.ispopulation:
                self.errormes = 'Не хватает населения для постройки!'
                return False
            if li[-3] + self.electricity > self.iselectricity:
                self.errormes = 'Не хватает электроэнергии для постройки!'
                return False
            pygame.draw.rect(screen, 'white', (200, 33, 100, 18), 0)
            pygame.draw.rect(screen, 'white', (350, 33, 100, 18), 0)
            pygame.display.flip()
            self.coins -= li[-1]
            self.electricity += li[-3]
            self.population += li[-2]
            self.mnojitel += li[4]
            self.hood()

        # todo если нет дороги...

        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, 'white', (50, 33, 80, 18), 0)
        text = font.render(str(self.coins), True, (255, 217, 25))
        screen.blit(text, (55, 33))
        return True

    def build(self, x, y, li):
        if self.updateparameters(li):
            buildimage = pygame.transform.scale(load_image(li[2]), (CELL_SIZE, CELL_SIZE))
            screen.blit(buildimage, (x * CELL_SIZE, y * CELL_SIZE + self.top))
            self.board[x][y][2] = li
        self.isbuilding = False
        pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
        font = pygame.font.Font(None, 25)
        text = font.render(self.errormes, True, (255, 0, 0))
        screen.blit(text, (500, 33))
        pygame.display.flip()


class Shop:
    def __init__(self, x: int, y: int, hw: int, image):
        self.opened = False
        self.screen = screen
        self.x = x
        self.y = y
        self.hw = hw
        self.image = image
        pygame.display.flip()

    def startshop(self):
        self.opened = True
        pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
        self.nowbuilding = ''
        self.copyscreen = screen.copy()
        pygame.draw.rect(screen, 'white', (100, 150,
                                                   800, 500), 0)
        self.type = 'дома'  # изначально открывается вкладка с домами
        self.openshop()
        self.housemenuim = pygame.transform.scale(load_image('house1.png'), (50, 50))
        self.electromenuim = pygame.transform.scale(load_image('electro.png'), (50, 50))
        self.othersmenuim = pygame.transform.scale(load_image('office.jpg'), (50, 50))
        self.closeim = pygame.transform.scale(load_image('close.png'), (50, 50))
        screen.blit(self.closeim, (850, 150))
        screen.blit(self.housemenuim, (850, 200))
        screen.blit(self.electromenuim, (850, 250))
        screen.blit(self.othersmenuim, (850, 300))
        pygame.display.flip()

    def openshop(self):
        if self.type == 'дома':
            pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                       750, 500), 0)
            self.drawbuildinginshop(0, 0, 'Частный домик', 'Прибыль: 10 Население: +8',
                                    'Требуемая электроэнергия: 1', '40',
                                    pygame.transform.scale(load_image('house1.png'),
                                                           (130, 130)))
            self.drawbuildinginshop(1, 0, 'Двухэтажный дом', 'Прибыль: 30 Население: +20',
                                    'Требуемая электроэнергия: 2', '150',
                                    pygame.transform.scale(load_image('house2.png'),
                                                           (130, 130)))
            self.drawbuildinginshop(2, 0, 'Многоквартирный дом', 'Прибыль: 100 Население: +40',
                                    'Требуемая электроэнергия: 3', '340',
                                    pygame.transform.scale(load_image('house3.png'),
                                                           (130, 130)))
        if self.type == 'электро':
            pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                       750, 500), 0)
            self.drawbuildinginshop(0, 0, 'Ветряк', 'Приносит электроэнергии: 5', 'Требуемое население: 0', '60',
                                    pygame.transform.scale(load_image('wind.png'), (130, 130)))
            self.drawbuildinginshop(1, 0, 'Солнечная панель', 'Приносит электроэнергии: 9', 'Требуемое население: 2',
                                    '125', pygame.transform.scale(load_image('solar.png'), (130, 130)))
            self.drawbuildinginshop(2, 0, 'Электростанция', 'Приносит электорэнергии: 16', 'Требуемое население: 3',
                                    '280', pygame.transform.scale(load_image('station.png'), (130, 130)))

        if self.type == 'службы':
            pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                       750, 500), 0)
            self.drawbuildinginshop(0, 0, 'Полицейский участок', 'Приносит: увеличение прибыли на 25%',
                                    'Требуемое население: 30, энергия: 7', '220',
                                    pygame.transform.scale(load_image('police.png'), (115, 115)))
            self.drawbuildinginshop(1, 0, '     Больница', 'Приносит: увеличение прибыли на 40%',
                                    'Требуемое население: 60, энергия: 13',
                                    '380', pygame.transform.scale(load_image('hospital.png'), (130, 130)))
            self.drawbuildinginshop(2, 0, 'Офисное здание', 'Приносит: увеличение прибыли на 55%',
                                    'Требуемое население: 100, энергия: 22',
                                    '650', pygame.transform.scale(load_image('office.jpg'), (130, 130)))

        pygame.display.flip()

    def drawbuildinginshop(self, row, col, name, par1, par2, cost, image):
        font1 = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 15)
        font3 = pygame.font.Font(None, 25)
        text1 = font1.render(name, True, (6, 128, 47))
        text2 = font2.render(par1, True, (0, 0, 0))
        text3 = font2.render(par2, True, (0, 0, 0))
        text4 = font3.render(cost, True, (255, 217, 25))
        screen.blit(image, (130 + 255 * row, 180 + 250 * col))
        screen.blit(pygame.transform.scale(load_image('coin.png'), (35, 35)), (170 + 250 * row, 340 + 250 * col))
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
            self.type = 'электро'
            self.openshop()
        if 850 <= pos[0] <= 900 and 300 <= pos[1] <= 350:
            self.type = 'службы'
            self.openshop()
        if 100 <= pos[0] <= 350 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[0]
            if self.type == 'электро':
                self.nowbuilding = board.buildlist[3]
            if self.type == 'службы':
                self.nowbuilding = board.buildlist[6]
            self.closeshop()
            board.isbuilding = True
        if 350 < pos[0] < 600 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[1]
            if self.type == 'электро':
                self.nowbuilding = board.buildlist[4]
            if self.type == 'службы':
                self.nowbuilding = board.buildlist[7]
            self.closeshop()
            board.isbuilding = True
        if 600 <= pos[0] <= 850 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.nowbuilding = board.buildlist[2]
            if self.type == 'электро':
                self.nowbuilding = board.buildlist[5]
            if self.type == 'службы':
                self.nowbuilding = board.buildlist[8]
            self.closeshop()
            board.isbuilding = True

    def closeshop(self):
        board.render()
        pygame.display.flip()
        self.opened = False


if __name__ == '__main__':
    balance = 1000
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')

    SIZE = WIDTH, HEIGHT = 1100, 750
    CELL_SIZE = 50
    TOP = 50
    RIGHT = 100

    screen = pygame.display.set_mode(SIZE)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    board = Board(1000 // CELL_SIZE, 700 // CELL_SIZE, screen, TOP, RIGHT)
    shop = Shop(999, 50, 100, 'shop.png')
    shopimage = pygame.transform.scale(load_image(shop.image), (shop.hw, shop.hw))

    clock = pygame.time.Clock()
    FPS = 60
    MAX_LEVEL = 10

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
            x, y = pygame.mouse.get_pos()
            if 1000 <= x <= 1100 and 50 <= y <= 150 and not shop.opened:
                pygame.draw.rect(screen, (88, 252, 88), (shop.x, shop.y, shop.hw, shop.hw), 0)
                screen.blit(shopimage, (1000, 50))
                pygame.display.flip()
            if not (1000 <= x <= 1100 and 50 <= y <= 150):
                pygame.draw.rect(screen, 'white', (shop.x, shop.y, shop.hw, shop.hw), 0)
                screen.blit(shopimage, (1000, 50))
                pygame.display.flip()
            if shop.opened:
                if 850 <= x <= 900 and 150 <= y <= 200:
                    pygame.draw.rect(screen, (88, 252, 88), (850, 150, 50, 50), 0)
                    screen.blit(shop.closeim, (850, 150))
                    pygame.display.flip()
                if 850 <= x <= 900 and 200 <= y <= 250:
                    pygame.draw.rect(screen, (88, 252, 88), (850, 200, 50, 50), 0)
                    screen.blit(shop.housemenuim, (850, 200))
                    pygame.display.flip()
                if 850 <= x <= 900 and 250 <= y <= 300:
                    pygame.draw.rect(screen, (88, 252, 88), (850, 250, 50, 50), 0)
                    screen.blit(shop.electromenuim, (850, 250))
                    pygame.display.flip()
                if 850 <= x <= 900 and 300 <= y <= 350:
                    pygame.draw.rect(screen, (88, 252, 88), (850, 300, 50, 50), 0)
                    screen.blit(shop.othersmenuim, (850, 300))
                    pygame.display.flip()
                if not (850 <= x <= 900 and 150 <= y <= 200):
                    pygame.draw.rect(screen, 'white', (850, 150, 50, 50), 0)
                    screen.blit(shop.closeim, (850, 150))
                    pygame.display.flip()
                if not (850 <= x <= 900 and 200 <= y <= 250):
                    pygame.draw.rect(screen, 'white', (850, 200, 50, 50), 0)
                    screen.blit(shop.housemenuim, (850, 200))
                    pygame.display.flip()
                if not (850 <= x <= 900 and 250 <= y <= 300):
                    pygame.draw.rect(screen, 'white', (850, 250, 50, 50), 0)
                    screen.blit(shop.electromenuim, (850, 250))
                    pygame.display.flip()
                if not (850 <= x <= 900 and 300 <= y <= 350):
                    pygame.draw.rect(screen, 'white', (850, 300, 50, 50), 0)
                    screen.blit(shop.othersmenuim, (850, 300))
                    pygame.display.flip()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()