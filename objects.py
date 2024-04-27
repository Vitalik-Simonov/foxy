import pygame as pg
from settings import *


# класс для поднимаемых предметов
class Fuel(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        # создание изображения для спрайта
        self.image = pg.image.load('data/fuel.png').convert_alpha()

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.collide_rect(self, self.game.player):
            self.game.score += 1
            self.kill()
