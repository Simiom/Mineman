import os
import sys
import pygame
import random

pygame.init()
size = width, height = 750, 650
screen = pygame.display.set_mode(size)

FPS = 50
Perx = Pery = 0
Perx2 = Pery2 = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('obsidian.png'),
    'empty': load_image('grass.png'),
    "destr_wall": load_image("stone.png")
}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(obsidian_group, all_sprites)
        elif tile_type == "empty":
            super().__init__(tiles_group, all_sprites)
        else:
            super().__init__(wall_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if self.tile_type == "destr_wall":
            if pygame.sprite.spritecollideany(self, vzriv):
                self.kill()
                level[self.rect.y // tile_width][self.rect.x // tile_width] = "."


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        global Perx
        Perx = self.rect.x - 15
        global Pery
        Pery = self.rect.y - 5
        self.boom = -1
        self.kol = 0

    def update(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:

                self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)
                elif self.rect.x < 0:
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

            if event.key == pygame.K_RIGHT:
                self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
                elif self.rect.x > width:
                    self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
            if event.key == pygame.K_UP:
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
                elif self.rect.y < 0:
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
            if event.key == pygame.K_DOWN:
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
                elif self.rect.y > height:
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
            global Perx
            Perx = self.rect.x - 15
            global Pery
            Pery = self.rect.y - 5


class Player2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        global Perx2
        Perx = self.rect.x - 15
        global Pery2
        Pery = self.rect.y - 5
        self.boom2 = -1
        self.kol2 = 0

    def update(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:

                self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)
                elif self.rect.x < 0:
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

            if event.key == pygame.K_d:
                self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
                elif self.rect.x > width:
                    self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
            if event.key == pygame.K_w:
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
                elif self.rect.y < 0:
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
            if event.key == pygame.K_s:
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + 50)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
                elif self.rect.y > height:
                    self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - 50)
            global Perx2
            Perx2 = self.rect.x - 15
            global Pery2
            Pery2 = self.rect.y - 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, map):
        super().__init__(enemy_group, all_sprites)
        self.image = load_image("enemy.png")
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.state = 0
        self.map = map

    def update(self):
        self.map = level
        if self.state == 0:
            self.state = random.randrange(1, 5)
        elif self.state == 1:
            if self.map[self.rect.y // tile_width + 1][self.rect.x // tile_width] == ".":
                self.rect.y += 5
            else:
                self.state = 0
        elif self.state == 2:
            if self.map[(self.rect.y + tile_width - 5) // tile_width - 1][self.rect.x // tile_width] == ".":
                self.rect.y -= 5
            else:
                self.state = 0
        elif self.state == 3:
            if self.map[self.rect.y // tile_width][self.rect.x // tile_width + 1] == ".":
                self.rect.x += 5
            else:
                self.state = 0
        elif self.state == 4:
            if self.map[self.rect.y // tile_width][(self.rect.x + tile_width - 5) // tile_width - 1] == ".":
                self.rect.x -= 5
            else:
                self.state = 0
        if pygame.sprite.spritecollideany(self, vzriv):
            self.kill()


# основной персонаж
player = None

# группы спрайтов
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

sprites = pygame.sprite.Group()
bomb = pygame.sprite.Sprite()
bomb.image = load_image("tnt.png")
bomb.rect = bomb.image.get_rect()
bomb.rect.x = 0
bomb.rect.y = -100
sprites.add(bomb)

bomb2 = pygame.sprite.Sprite()
bomb2.image = load_image("tnt.png")
bomb2.rect = bomb2.image.get_rect()
bomb2.rect.x = 0
bomb2.rect.y = -100
sprites.add(bomb2)

all_sprites = pygame.sprite.Group()

wall_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
obsidian_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
vzriv = pygame.sprite.Group()
deadscreen = pygame.sprite.Group()

Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == ',':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                new_player2 = Player2(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, new_player2, x, y


def smert(boom):
    global end
    if pygame.sprite.spritecollideany(boom, player_group):
        end = True


level = [[]]


def spawn_all(numen, numbl, levelr):
    for a in range(len(levelr)):
        for i in levelr[a]:
            level[a].append(i)
        level.append([])

    for _ in range(numbl):
        x = 0
        y = 0
        while level[y][x] != ".":
            y = random.randrange(0, len(level) - 1)
            x = random.randrange(0, len(level[0]) - 1)
        Tile("destr_wall", x, y)
        level[y][x] = "$"

    for _ in range(numen):
        x = 0
        y = 0
        while level[y][x] != ".":
            y = random.randrange(0, len(level) - 1)
            x = random.randrange(0, len(level[0]) - 1)
        Enemy(x, y, level)


def BoomKrest(x, y, kill=False):
    global vzriv
    global end
    if kill == False:
        # ==============center=====================
        boom_image = load_image("center.png")
        boom = pygame.sprite.Sprite(all_sprites)
        boom.image = boom_image
        boom.rect = boom.image.get_rect()
        boom.rect.x = x
        boom.rect.y = y

        if pygame.sprite.spritecollideany(boom, obsidian_group):
            boom.rect.x = 0
            boom.rect.y = -100
        smert(boom)
        vzriv.add(boom)
        vzriv.draw(screen)
        # ===================Left1================
        boom_image = load_image("boom.png")
        boom = pygame.sprite.Sprite(all_sprites)
        boom.image = boom_image
        boom.rect = boom.image.get_rect()
        boom.rect.x = x - 50
        boom.rect.y = y
        if pygame.sprite.spritecollideany(boom, obsidian_group):
            boom.rect.x = 0
            boom.rect.y = -100
        else:
            smert(boom)
            vzriv.add(boom)
            vzriv.draw(screen)
            # ==================Left2=================
            boom_image = load_image("boom.png")
            boom = pygame.sprite.Sprite(all_sprites)
            boom.image = boom_image
            boom.rect = boom.image.get_rect()
            boom.rect.x = x - 100
            boom.rect.y = y
            if pygame.sprite.spritecollideany(boom, obsidian_group):
                boom.rect.x = 0
                boom.rect.y = -100
            else:
                smert(boom)
                vzriv.add(boom)
                vzriv.draw(screen)
        # =================Right1==================
        boom_image = load_image("boom.png")
        boom = pygame.sprite.Sprite(all_sprites)
        boom.image = boom_image
        boom.rect = boom.image.get_rect()
        boom.rect.x = x + 50
        boom.rect.y = y
        if pygame.sprite.spritecollideany(boom, obsidian_group):
            boom.rect.x = 0
            boom.rect.y = -100
        else:
            smert(boom)
            vzriv.add(boom)
            vzriv.draw(screen)
            # ==================Right2=================
            boom_image = load_image("boom.png")
            boom = pygame.sprite.Sprite(all_sprites)
            boom.image = boom_image
            boom.rect = boom.image.get_rect()
            boom.rect.x = x + 100
            boom.rect.y = y
            if pygame.sprite.spritecollideany(boom, obsidian_group):
                boom.rect.x = 0
                boom.rect.y = -100
            else:
                smert(boom)
                vzriv.add(boom)
                vzriv.draw(screen)
        # ================Up1===================
        boom_image = load_image("boomUp.png")
        boom = pygame.sprite.Sprite(all_sprites)
        boom.image = boom_image
        boom.rect = boom.image.get_rect()
        boom.rect.x = x
        boom.rect.y = y - 50
        if pygame.sprite.spritecollideany(boom, obsidian_group):
            boom.rect.x = 0
            boom.rect.y = -100
        else:
            smert(boom)
            vzriv.add(boom)
            vzriv.draw(screen)
            # =================Up2==================
            boom_image = load_image("boomUp.png")
            boom = pygame.sprite.Sprite(all_sprites)
            boom.image = boom_image
            boom.rect = boom.image.get_rect()
            boom.rect.x = x
            boom.rect.y = y - 100
            if pygame.sprite.spritecollideany(boom, obsidian_group):
                boom.rect.x = 0
                boom.rect.y = -100
            else:
                smert(boom)
                vzriv.add(boom)
                vzriv.draw(screen)
        # =================Down1==================
        boom_image = load_image("boomUp.png")
        boom = pygame.sprite.Sprite(all_sprites)
        boom.image = boom_image
        boom.rect = boom.image.get_rect()
        boom.rect.x = x
        boom.rect.y = y + 50
        if pygame.sprite.spritecollideany(boom, obsidian_group):
            boom.rect.x = 0
            boom.rect.y = -100
        else:
            smert(boom)
            vzriv.add(boom)
            vzriv.draw(screen)
            # ==================Down2=================
            boom_image = load_image("boomUp.png")
            boom = pygame.sprite.Sprite(all_sprites)
            boom.image = boom_image
            boom.rect = boom.image.get_rect()
            boom.rect.x = x
            boom.rect.y = y + 100
            if pygame.sprite.spritecollideany(boom, obsidian_group):
                boom.rect.x = 0
                boom.rect.y = -100
            else:
                smert(boom)
                vzriv.add(boom)
                vzriv.draw(screen)
    else:

        vzriv = pygame.sprite.Group()




kol = 0  # кол-во смен картинки бомбы
boom = False  # флаг взрыва
boomX = 0  # кординаты центра взрыва
boomY = 0

kol2 = 0  # кол-во смен картинки бомбы
boom2 = False  # флаг взрыва
boomX2 = 0  # кординаты центра взрыва
boomY2 = 0

q = w = 0
end = False

timeboom = -1  # время взрыва
n = -1  # номер картинки
timeboom2 = -1  # время взрыва
n2 = -1  # номер картинки

start_screen()
clock = pygame.time.Clock()
main_player, second_player, x, y = generate_level(load_level('level.txt'))
spawn_all(10, 10, load_level('level.txt'))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and n2 == -1:
                bomb2.rect.x = Perx2
                bomb2.rect.y = Pery2
                boomX2 = Perx2
                boomY2 = Pery2
                kol2 = 0
                n2 = 0
                sprites.draw(screen)
            if event.key == pygame.K_p and n == -1:
                bomb.rect.x = Perx
                bomb.rect.y = Pery
                boomX = Perx
                boomY = Pery
                kol = 0
                n = 0
                sprites.draw(screen)
            else:
                player_group.update()
    if n == 0:
        if kol == 5:
            bomb.rect.x = 0
            bomb.rect.y = -100
            n = -1
            boom = True
        else:
            bomb.image = load_image("tnt.png")
            n = 1
    elif n == 1:
        bomb.image = pygame.transform.scale(load_image("tnt.png"), (48, 52))
        n = 2
    elif n == 2:
        bomb.image = pygame.transform.scale(load_image("tnt.png"), (52, 48))
        n = 0
        kol += 1

    if n2 == 0:
        if kol2 == 5:
            bomb2.rect.x = 0
            bomb2.rect.y = -100
            n2 = -1
            boom2 = True
        else:
            bomb2.image = load_image("tnt.png")
            n2 = 1
    elif n2 == 1:
        bomb2.image = pygame.transform.scale(load_image("tnt.png"), (48, 52))
        n2 = 2
    elif n2 == 2:
        bomb2.image = pygame.transform.scale(load_image("tnt.png"), (52, 48))
        n2 = 0
        kol2 += 1

    if boom:
        BoomKrest(boomX, boomY)
        boom = False
        timeboom = 0

    if boom2:
        BoomKrest(boomX2, boomY2)
        boom2 = False
        timeboom2 = 0

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    wall_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    sprites.draw(screen)
    enemy_group.update()
    wall_group.update()
    if timeboom != -1:
        vzriv.draw(screen)
        timeboom += 1
    if timeboom == 10:
        timeboom = -1
        BoomKrest(0, 0, True)

    if timeboom2 != -1:
        vzriv.draw(screen)
        timeboom2 += 1
    if timeboom2 == 10:
        timeboom2 = -1
        BoomKrest(0, 0, True)

    if pygame.sprite.spritecollideany(main_player, enemy_group):
        end = True
    if pygame.sprite.spritecollideany(second_player, enemy_group):
        end = True
    if end:
        dead_image = load_image("dead.png")
        dead = pygame.sprite.Sprite(all_sprites)
        dead.image = dead_image
        dead.rect = dead.image.get_rect()
        if q < 750:
            dead.rect.x = 750 - q
            dead.rect.y = 650 - w
        q += 18
        w += 15
        deadscreen.add(dead)
        deadscreen.draw(screen)

    pygame.display.flip()
    clock.tick(10)
