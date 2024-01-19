import pygame
import os
import sys
import traceback


def load_image(name, colorkey=None):
    fullname = os.path.join('data_images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_sound(name):
    fullname = os.path.join('sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound


class Road(pygame.sprite.Sprite):
    image = load_image("roads.png")

    def __init__(self, group: pygame.sprite.Group, x: int, y: int):
        super().__init__(group)
        self.x, self.y = x, y

        self.image = Road.image.subsurface((250, 0, 250, 250))
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE + TOP)
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


class House(Building):
    def __init__(self, group, x, y, building_cost, start_income, ispopulation, electrcity):
        super().__init__(group, x, y, building_cost, start_income)

        self.x, self.y = x, y
        self.lvl = 0
        self.income = start_income
        self.image = Building.image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE + TOP)
        self.building_cost = building_cost
        self.upgrade_cost = building_cost

        self.population = ispopulation
        board.coins -= building_cost
        board.electricity += electrcity
        board.ispopulation += self.population

    def __repr__(self):
        return "H"


class Electricity(Building):
    def __init__(self, group, x, y, building_cost, start_income, population, iselectrcity):
        super().__init__(group, x, y, building_cost, start_income)
        self.x, self.y = x, y
        self.lvl = 0
        self.image = Building.image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE + TOP)
        self.building_cost = building_cost
        self.upgrade_cost = building_cost
        board.coins -= building_cost
        board.iselectricity += iselectrcity
        board.population += population


class Service(Building):
    def __init__(self, group, x, y, building_cost, start_income, population, electrcity, mnojitel):
        super().__init__(group, x, y, building_cost, start_income)
        self.x, self.y = x, y
        self.lvl = 0
        self.image = Building.image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * CELL_SIZE, self.y * CELL_SIZE + TOP)
        self.building_cost = building_cost
        self.upgrade_cost = building_cost
        board.mnojitel += mnojitel
        board.coins -= building_cost
        board.electricity += electrcity
        board.population += population


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
        self.coins = 10000
        self.width = width
        self.height = height
        self.board = [[Field(x, y) for x in range(width)] for y in range(height)]
        self.screen = screen
        self.render()
        self.hood()
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
        return x // CELL_SIZE, (y - TOP) // CELL_SIZE

    def render(self):
        boardfield = pygame.transform.scale(load_image('fon-trava.png'), (1000, 700))
        screen.blit(boardfield, (0, self.top))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (CELL_SIZE * j, CELL_SIZE * i + self.top,
                                                   CELL_SIZE, CELL_SIZE), 1)

    def hood(self):
        pygame.draw.rect(screen, 'white', (0, 0, 200, 50))
        pygame.draw.rect(screen, 'white', (200, 33, 100, 18), 0)
        pygame.draw.rect(screen, 'white', (350, 33, 100, 18), 0)
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

    def houseupdateparameters(self, cost, el):
        self.errormes = ''
        if self.coins - cost < 0:
            self.errormes = 'Не хватает денег для постройки!'
            return False
        if el + self.electricity > self.iselectricity:
            self.errormes = 'Не хватает электроэнергии для постройки!'
            return False
        return True

    def electroupdateparameters(self, cost, people):
        self.errormes = ''
        if self.coins - cost < 0:
            self.errormes = 'Не хватает денег для постройки!'
            return False
        if people + self.population > self.ispopulation:
            self.errormes = 'Не хватает населения для постройки!'
            return False
        return True

    def serviceupdateparameters(self, cost, people, el):
        self.errormes = ''
        if self.coins - cost < 0:
            self.errormes = 'Не хватает денег для постройки!'
            return False
        if people + self.population > self.ispopulation:
            self.errormes = 'Не хватает населения для постройки!'
            return False
        if el + self.electricity > self.iselectricity:
            self.errormes = 'Не хватает электроэнергии для постройки!'
            return False
        return True

    def build(self, x, y, item):
        if shop.type == 'электро':
            electro_sound.play()
        building_sound.play()
        board[y][x] = item
        buildings.draw(screen)
        pygame.display.flip()
        board.isbuilding = False
        board.hood()


class Shop:
    def __init__(self, x: int, y: int, hw: int, image):
        self.opened = False
        self.screen = screen
        self.x = x
        self.y = y
        self.hw = hw
        self.shopimage = load_image(image)
        pygame.draw.rect(screen, (8, 204, 78), (self.x, self.y, self.hw + 1, self.hw), 0)
        self.shopimage = pygame.transform.scale(self.shopimage, (hw, hw))
        screen.blit(self.shopimage, (1000, 50))
        pygame.display.flip()

    def startshop(self):
        self.opened = True
        pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
        self.nowbuilding = ''
        self.copyscreen = screen.copy()
        pygame.draw.rect(screen, (255, 255, 255), (100, 150,
                                                   800, 500), 0)
        self.type = 'дома'  # изначально открывается вкладка с домами
        self.openshop()
        self.shopimage = pygame.transform.scale(load_image('shop.png'), (100, 100))
        self.housemenuim = pygame.transform.scale(load_image('house1.png'), (50, 50))
        self.electromenuim = pygame.transform.scale(load_image('electro.png'), (50, 50))
        self.othersmenuim = pygame.transform.scale(load_image('office.jpg'), (50, 50))
        self.closeim = pygame.transform.scale(load_image('close.png'), (50, 50))
        screen.blit(self.closeim, (850, 150))
        screen.blit(self.housemenuim, (850, 200))
        screen.blit(self.electromenuim, (850, 250))
        screen.blit(self.othersmenuim, (850, 300))
        pygame.display.flip()
        self.selected = None

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
            self.drawbuildinginshop(1, 0, 'Солнечная панель', 'Приносит электроэнергии: 9', 'Требуемое население: 4',
                                    '125', pygame.transform.scale(load_image('solar.png'), (130, 130)))
            self.drawbuildinginshop(2, 0, 'Электростанция', 'Приносит электорэнергии: 16', 'Требуемое население: 7',
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
            return
        elif 850 <= pos[0] <= 900 and 200 <= pos[1] <= 250:
            self.type = 'дома'
            self.openshop()
        elif 850 <= pos[0] <= 900 and 250 <= pos[1] <= 300:
            self.type = 'электро'
            self.openshop()
        elif 850 <= pos[0] <= 900 and 300 <= pos[1] <= 350:
            self.type = 'службы'
            self.openshop()
        elif 100 <= pos[0] <= 350 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.checkhousebuilding(40, 10, 8, 1, 'house1.png')
            if self.type == 'электро':
                self.checkelectrobuilding(30, 0, 5, 'wind.png')
            if self.type == 'службы':
                self.checkservicebuilding(220, 0.25, 30, 7, 'police.png')
        elif 350 < pos[0] < 600 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.checkhousebuilding(150, 30, 20, 2, 'house2.png')
            if self.type == 'электро':
                self.checkelectrobuilding(125, 4, 9, 'solar.png')
            if self.type == 'службы':
                self.checkservicebuilding(380, 0.4, 60, 13, 'hospital.png')
        elif 600 <= pos[0] <= 850 and 150 <= pos[1] <= 400:
            if self.type == 'дома':
                self.checkhousebuilding(340, 100, 40, 3, 'house3.png')
            if self.type == 'электро':
                self.checkelectrobuilding(280, 7, 16, 'station.png')
            if self.type == 'службы':
                self.checkservicebuilding(650, 0.55, 100, 22, 'office.jpg')

    def checkhousebuilding(self, cost, income, population, electricity, image):
        bool = board.houseupdateparameters(cost, electricity)
        if bool:
            item = House(buildings, 0, 0, cost, income, population, electricity)
            item.set_image(image)
            self.selected = item
            self.commitbuliding()
        if not bool:
            pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
            font = pygame.font.Font(None, 25)
            text = font.render(str(board.errormes), True, 'red')
            screen.blit(text, (500, 33))

    def checkelectrobuilding(self, cost, population, electricity, image):
        bool = board.electroupdateparameters(cost, population)
        if bool:
            income = 0  # не дает прибыли, нужно только для инициализации родительского класса класса building
            item = Electricity(buildings, 0, 0, cost, income, population, electricity)
            item.set_image(image)
            self.selected = item
            self.commitbuliding()
        if not bool:
            pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
            font = pygame.font.Font(None, 25)
            text = font.render(str(board.errormes), True, 'red')
            screen.blit(text, (500, 33))

    def checkservicebuilding(self, cost, mnojitel, population, electricity, image):
        bool = board.serviceupdateparameters(cost, population, electricity)
        if bool:
            income = 0  # не дает прибыли, нужно только для инициализации родительского класса класса building
            item = Service(buildings, 0, 0, cost, income, population, electricity, mnojitel)
            item.set_image(image)
            self.selected = item
            self.commitbuliding()
        if not bool:
            pygame.draw.rect(screen, 'white', (500, 0, 500, 51), 0)
            font = pygame.font.Font(None, 25)
            text = font.render(str(board.errormes), True, 'red')
            screen.blit(text, (500, 33))

    def commitbuliding(self):
        buildings.remove_internal(self.selected)
        self.closeshop()
        buildings.draw(screen)
        pygame.display.flip()
        buildings.add(self.selected)
        board.isbuilding = True

    def closeshop(self):
        board.render()
        pygame.display.flip()
        buildings.draw(screen)
        self.opened = False


class Roadshop():
    def __init__(self, x, y, hw, image):
        self.x, self.y, self.hw = x, y, hw
        self.isbuilding = False
        self.roadimage = pygame.transform.scale(load_image(image), (100, 100))
        screen.blit(self.roadimage, (1000, 150))

    def build(self):
        print('buildroad')

def excepthook(exc_type, exc_value, exc_tb):  # для показа ошибок
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = excepthook

if __name__ == '__main__':
    balance = 1000
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')

    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    building_sound = load_sound('building.ogg')
    building_sound.set_volume(0.09)
    click_sound = load_sound("click.wav")
    click_sound.set_volume(0.1)
    electro_sound = load_sound("electro.ogg")
    electro_sound.set_volume(0.07)

    SIZE = WIDTH, HEIGHT = 1100, 750
    CELL_SIZE = 50
    TOP = 50
    RIGHT = 100

    screen = pygame.display.set_mode(SIZE)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    board = Board(1000 // CELL_SIZE, 700 // CELL_SIZE, screen, TOP, RIGHT)
    shop = Shop(999, 50, 100, 'shop.png')
    roadshop = Roadshop(999, 150, 100, 'roadshop.png')

    clock = pygame.time.Clock()
    FPS = 60
    MAX_LEVEL = 10

    buildings = pygame.sprite.Group()
    roads = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            x, y = pygame.mouse.get_pos()
            if 1000 <= x <= 1100 and 50 <= y <= 150 and not shop.opened:
                pygame.draw.rect(screen, (88, 252, 88), (shop.x, shop.y, shop.hw, shop.hw), 0)
                screen.blit(shop.shopimage, (1000, 50))
                pygame.display.flip()
            if not (1000 <= x <= 1100 and 50 <= y <= 150):
                pygame.draw.rect(screen, 'white', (shop.x, shop.y, shop.hw, shop.hw), 0)
                screen.blit(shop.shopimage, (1000, 50))
                pygame.display.flip()
            if 1000 <= x <= 1100 and 150 <= y <= 250 and not shop.opened:
                pygame.draw.rect(screen, (88, 252, 88), (roadshop.x, roadshop.y, roadshop.hw, roadshop.hw), 0)
                screen.blit(roadshop.roadimage, (1000, 150))
                pygame.display.flip()
            if not (1000 <= x <= 1100 and 150 <= y <= 250) and not shop.opened:
                pygame.draw.rect(screen, 'white', (roadshop.x, roadshop.y, roadshop.hw, roadshop.hw), 0)
                screen.blit(roadshop.roadimage, (1000, 150))
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if event.button == pygame.BUTTON_LEFT:
                    if board.isbuilding:
                        x, y = board.click_pos()
                        if 0 <= x <= board.width and 0 <= y <= board.height:
                            if type(board[y][x]) == Field:
                                item = shop.selected
                                item.rect = item.rect.move(x * CELL_SIZE, y * CELL_SIZE)
                                board.build(x, y, item)
                if not shop.opened and not board.isbuilding and not roadshop.isbuilding:
                    if 1000 <= event.pos[0] <= 1100 and 50 <= event.pos[1] <= 150:
                        shop.startshop()
                if not shop.opened and not board.isbuilding and not roadshop.isbuilding:
                    if 1000 <= event.pos[0] <= 1100 and 150 <= event.pos[1] <= 250:
                        roadshop.isbuilding = True
                        roadshop.build()
                else:
                    shop.shopclickreact(event.pos)
        buildings.update()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
