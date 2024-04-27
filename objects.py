import pygame as pg
from settings import *


# класс для топлива
class Fuel(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        # создание изображения для спрайта
        self.image = pg.image.load('data/fuel.png').convert_alpha()

        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.collide_mask(self, self.game.player):
            self.game.fuel += 1
            self.kill()


class Gear(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        # создание изображения для спрайта
        self.image = pg.image.load('data/gear.png').convert_alpha()

        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.collide_mask(self, self.game.player):
            self.game.gear += 1
            self.kill()


class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        # создание изображения для спрайта
        self.image = pg.image.load('data/box.png').convert_alpha()

        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.collide_mask(self, self.game.player):
            self.game.box += 1
            self.kill()


class Rocket(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        # создание изображения для спрайта
        self.image = pg.image.load('data/rocket.png').convert_alpha()

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pg.sprite.collide_rect(self, self.game.player):
            if self.game.fuel >= TARGET_FUEL and self.game.gear >= TARGET_GEAR and self.game.box >= TARGET_BOX:
                self.game.running = False
                self.game.winning = True
