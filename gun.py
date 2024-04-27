import pygame as pg
from math import *
from time import time
from settings import *


class Rotate_object(pg.sprite.Sprite):
    def __init__(self, game, master, image, delta, l):
        self.game = game
        self.master = master
        self.delta = delta
        self.l = l
        super().__init__(game.all_sprites)
        self.image = image
        self.orig = self.image.copy()

        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.x = self.master.rect.centerx
        self.y = self.master.rect.centery
        self.angle = 90
        self.x += (self.l // 2 + self.delta)
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.spawnx = self.l + self.delta + self.master.rect.centerx
        self.spawny = self.master.rect.centery

    def update(self):
        self.update_by_angle()

    def update_by_angle(self):
        self.angle %= 360
        if 90 <= self.angle <= 270:
            self.image = pg.transform.rotate(pg.transform.flip(self.orig, 0, 1), -self.angle)
        else:
            self.image = pg.transform.rotate(self.orig, -self.angle)
        self.rect = self.image.get_rect()
        self.x = self.master.rect.centerx
        self.y = self.master.rect.centery
        self.x += (self.delta + self.l // 2) * cos(radians(self.angle))
        self.y += (self.delta + self.l // 2) * sin(radians(self.angle))
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.spawnx = self.master.rect.centerx
        self.spawny = self.master.rect.centery
        self.spawnx += (self.delta + self.l) * cos(radians(self.angle))
        self.spawny += (self.delta + self.l) * sin(radians(self.angle))


class Gun(Rotate_object):
    def __init__(self, game, master):
        im = pg.image.load('data/gun.png')
        im.convert_alpha()
        super().__init__(game, master, im, 0, im.get_width())
        self.speed = 0.5
        self.last = time()
        self.last_drone = 0

    def update(self):
        x, y = pg.mouse.get_pos()
        x += self.game.camera.x - WIDTH // 2
        y += self.game.camera.y - HEIGHT // 2
        x -= self.master.rect.centerx
        y -= self.master.rect.centery
        try:
            if y < 0:
                self.angle = 360 - degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
            else:
                self.angle = degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
        except:
            self.angle = 0
        self.update_by_angle()

        if pg.mouse.get_pressed(3)[0]:
            self.shot()
        if pg.key.get_pressed()[pg.K_SPACE]:
            self.drone()

    def shot(self):
        if time() - self.last >= self.speed:
            self.game.sound.play('shot')
            b = Bullet(self.game, self)
            self.last = time()

    def drone(self):
        if time() - self.last_drone >= self.speed:
            self.game.sound.play('shot')
            b = Drone(self.game, self)
            self.game.camera.target = b
            self.last_drone = time()


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, gun, speed=1000, damage=2):
        super().__init__(game.all_sprites)
        self.game = game
        self.gun = gun
        self.speed = speed
        self.damage = damage
        self.x = self.gun.spawnx
        self.y = self.gun.spawny
        self.angle = self.gun.angle
        self.image = pg.image.load('data/bullet.png').convert_alpha()
        self.image = pg.transform.rotate(self.image, -self.angle)

        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.x += self.speed * cos(radians(self.angle)) / self.game.fps
        self.y += self.speed * sin(radians(self.angle)) / self.game.fps
        self.rect.x = self.x
        self.rect.y = self.y
        if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]): # Проверка на столкновение:
            self.kill()
        self.check()

    def check(self):
        s = pg.sprite.spritecollide(self, self.game.enemies, False)
        if s:
            self.kill()
            s[0].damage(self.damage)


class Drone(pg.sprite.Sprite):
    def __init__(self, game, gun, speed=1000, damage=2):
        super().__init__(game.all_sprites)
        self.game = game
        self.gun = gun
        self.speed = speed
        self.damage = damage
        self.x = self.gun.spawnx  # координаты
        self.y = self.gun.spawny
        self.spawnx = self.x # координаты спавна
        self.spawny = self.y
        self.angle = self.gun.angle
        self.image = pg.image.load('data/drone.png').convert_alpha()  # создание изображения для спрайта
        self.image = pg.transform.rotate(self.image, -self.angle)  # поворот спрайта

        self.mask = pg.mask.from_surface(self.image)  # создание маски для спрайта

        self.rect = self.image.get_rect()  # создание хитбокса для спрайта
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.x += self.speed * cos(radians(self.angle)) / self.game.fps
        self.y += self.speed * sin(radians(self.angle)) / self.game.fps
        self.rect.x = self.x
        self.rect.y = self.y
        if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]): # Проверка на столкновение:
            self.kill()
        if (self.x - self.spawnx) ** 2 + (self.y - self.spawny) ** 2 > 1000 ** 2:
            self.kill()
