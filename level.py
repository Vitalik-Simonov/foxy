from settings import *
import pygame as pg
from objects import *


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


def load_platforms(game):
    platforms = []
    level_load = open('data\\level.txt', 'r').readlines() # читаем уровень
    for platform in level_load:
        t, x, y = platform.rstrip('\n').split() # тип, координата х, координата у
        if t == 'static':
            platforms.append(Platform(game, int(x), int(y)))
        elif t == 'fuel':
            Fuel(game, int(x), int(y))
    return platforms
