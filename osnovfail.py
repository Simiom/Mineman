import os
import sys
import pygame
import random


pygame.init()
pygame.mixer.init()
size = width, height = 750, 650
screen = pygame.display.set_mode(size)

FPS = 50
Perx = Pery = 0

music = ["data/den_pobedi.wav","data/Was_Wollen.wav","data/den_pobedi.wav"]
music_num = 0
def play_music():
    global music_num
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music[music_num])
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    if music_num == 2:
        music_num =0
    else:
        music_num +=1


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
    play_music()
    fon = pygame.transform.scale(load_image('Fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    baton = pygame.sprite.Group()
    play_image = load_image("play.png")
    play = pygame.sprite.Sprite(baton)
    play.image = play_image
    play.rect = play.image.get_rect()
    baton.add(play)
    play.rect.x = 542
    play.rect.y = 307

    menu_image = load_image("menu.png")
    menu = pygame.sprite.Sprite(baton)
    menu.image = menu_image
    menu.rect = menu.image.get_rect()
    baton.add(menu)
    menu.rect.x = 542
    menu.rect.y = 507

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                if play.rect.collidepoint(event.pos):
                    play.image = pygame.transform.scale(load_image("play.png"), (150, 75))

                else:
                    play.image = play_image
                if menu.rect.collidepoint(event.pos):
                    menu.image = pygame.transform.scale(load_image("menu.png"), (150, 75))

                else:
                    menu.image = menu_image
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play.rect.collidepoint(event.pos):
                    play_music()
                    return  # пошла игра
                elif menu.rect.collidepoint(event.pos):
                    run = True
                    Menu = pygame.transform.scale(load_image('FonMenu.png'), (width, height))
                    batonvmenu = pygame.sprite.Group()
                    vstroi_image = load_image("vstroi.png")
                    vstroi = pygame.sprite.Sprite(baton)
                    vstroi.image = vstroi_image
                    vstroi.rect = vstroi.image.get_rect()
                    batonvmenu.add(vstroi)
                    vstroi.rect.x = 285
                    vstroi.rect.y = 569
                    screen.blit(Menu, (0, 0))
                    while run:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                terminate()
                            elif event.type == pygame.MOUSEMOTION:
                                if vstroi.rect.collidepoint(event.pos):
                                    vstroi.image = pygame.transform.scale(load_image("vstroi.png"), (150, 60))
                                else:
                                    vstroi.image = vstroi_image
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if vstroi.rect.collidepoint(event.pos):
                                    run = False
                                    vstroi.kill()
                        screen.blit(Menu, (0, 0))
                        batonvmenu.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        screen.blit(fon, (0, 0))
        baton.draw(screen)
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
player_image2 = load_image('mario2.png')
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

    def update(self, kill = False):
        if self.tile_type == "destr_wall":
            if pygame.sprite.spritecollideany(self, vzriv):
                self.kill()
                level[self.rect.y // tile_width][self.rect.x // tile_width] = "."
        if kill: self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.type = "rus"
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

    def update(self,kill = False):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.image = pygame.transform.flip(player_image, True, False)
                self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)

                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

                elif self.rect.x < 0:
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

            if event.key == pygame.K_d:
                self.image = player_image
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
            global Perx
            Perx = self.rect.x - 15
            global Pery
            Pery = self.rect.y - 5
        if kill: self.kill()


class Player2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.type = "nem"
        super().__init__(player_group, all_sprites)
        self.image = player_image2
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        global Perx2
        Perx = self.rect.x - 15
        global Pery2
        Pery = self.rect.y - 5
        self.boom2 = -1
        self.kol2 = 0

    def update(self, kill = False):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.image = player_image2
                self.rect = self.image.get_rect().move(self.rect.x - 50, self.rect.y)
                if pygame.sprite.spritecollideany(self, obsidian_group) or pygame.sprite.spritecollideany(self,
                                                                                                          wall_group):
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

                elif self.rect.x < 0:
                    self.rect = self.image.get_rect().move(self.rect.x + 50, self.rect.y)

            if event.key == pygame.K_RIGHT:
                self.image = pygame.transform.flip(player_image2, True, False)
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
            global Perx2
            Perx2 = self.rect.x - 15
            global Pery2
            Pery2 = self.rect.y - 5
        if kill: self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, map):
        super().__init__(enemy_group, all_sprites)
        self.image = load_image("enemy.png")
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.state = 0
        self.map = map

    def update(self, kill = False):
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
        if kill: self.kill()

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

nem = False
def smert(boom):
    global end
    global nem
    collide = pygame.sprite.spritecollideany(boom, player_group)
    if collide:
        nem = collide.type == "nem"
        end = True


level = [[]]


def spawn_all(numen, numbl, levelr):
    global level
    level = [[]]
    for a in range(len(levelr)):
        for i in levelr[a]:
            level[a].append(i)
        level.append([])
    print(level)
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

runprogram = True
while runprogram:
    print(1)
    baton = pygame.sprite.Group()
    inmanu_image = load_image("inmanu.png")
    inmanu = pygame.sprite.Sprite(baton)
    inmanu.image = inmanu_image
    inmanu.rect = inmanu.image.get_rect()
    baton.add(inmanu)

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
    reset = False

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
                if event.key == pygame.K_KP0 and n2 == -1:
                    bomb2.rect.x = Perx2
                    bomb2.rect.y = Pery2
                    boomX2 = Perx2
                    boomY2 = Pery2
                    kol2 = 0
                    n2 = 0
                    sprites.draw(screen)
                if event.key == pygame.K_e and n == -1:
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
            if nem:
                fon = pygame.transform.scale(load_image('nem.png'), (width, height))
            else:
                fon = pygame.transform.scale(load_image('dead.png'), (width, height))
            screen.blit(fon, (0, 0))
            inmanu.rect.x = 300
            inmanu.rect.y = 548
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEMOTION:
                    if inmanu.rect.collidepoint(event.pos):
                        inmanu.image = pygame.transform.scale(load_image("inmanu.png"), (150, 75))
                    else:
                        inmanu.image = inmanu_image
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inmanu.rect.collidepoint(event.pos):
                        end = False
                        reset = True
                        enemy_group.update(True)
                        player_group.update(True)
                        wall_group.update(True)
                        break  # игра заново
            baton.draw(screen)
            pygame.display.flip()
        if reset:
            break
        pygame.display.flip()
        clock.tick(10)
