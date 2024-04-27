from settings import *
import pygame as pg
from objects import *
from mobs import *


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(self.game.all_sprites)
        # создание изображения для спрайта
        self.image = pg.image.load(f'data\\platform.png').convert_alpha()
        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)
        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class MovePlatform(Platform):
    def __init__(self, game, x, y, l):
        self.game = game
        super().__init__(game, x, y)
        self.image = pg.image.load('data\\move_platform.png').convert_alpha()  # загрузка изображения
        self.mask = pg.mask.from_surface(self.image)  # создание маски для спрайта
        self.l = l  # длина пути перемещения платформы
        self.start_x = x
        self.x = x
        self.direction = 1

    def update(self):
        if self.rect.x < self.start_x + self.l and self.direction == 1:
            self.x += 100 / self.game.fps  # Учитываем FPS
        elif self.rect.x > self.start_x:
            self.x -= 100 / self.game.fps  # Учитываем FPS
            self.direction = -1
        else:
            self.direction = 1
        self.rect.x = self.x
        if pg.sprite.collide_mask(self, self.game.player):  # Если спрайт столкнулся с игроком
            while pg.sprite.collide_mask(self, self.game.player):  # Пока спрайт касается игрока
                if self.direction == 1:  # Если спрайт двигается вправо
                    self.game.player.x += 1  # Игрок двигается вправо
                else:
                    self.game.player.x -= 1  # Игрок двигается влево
                self.game.player.rect.x = self.game.player.x  # Обновляем координаты спрайта



# загрузка уровня
def load_platforms(game):
    platforms = []
    level_load = open('data\\level.txt', 'r').readlines() # читаем уровень
    for platform in level_load:
        t, x, y, *args = platform.rstrip('\n').split() # тип, координата х, координата у
        if t == 'static':
            platforms.append(Platform(game, int(x), int(y)))
        elif t == 'move':
            platforms.append(MovePlatform(game, int(x), int(y), int(args[0])))
        elif t == 'fuel':
            Fuel(game, int(x), int(y))
        elif t == 'rocket':
            Rocket(game, int(x), int(y))
        elif t == 'enemy':
            Enemy(game, (int(x), int(y)))
    return platforms
