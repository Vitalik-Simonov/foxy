import pygame as pg
from settings import *
import time


class Mob(pg.sprite.Sprite):
    def __init__(self, game, pos, health, image, *args):
        super().__init__(game.all_sprites, game.mobs, *args)
        self.is_live = True # жив ли спрайт
        self.game = game
        self.health = health # здоровье спрайта
        self.x = pos[0] # координаты спрайта
        self.y = pos[1]
        self.image = image # изображение спрайта
        self.rect = self.image.get_rect()
        self.rect.x = self.x # координаты спрайта
        self.rect.y = self.y
        self.mask = pg.mask.from_surface(self.image) # маска спрайта
        self.speed_x = 0 # компоненты скорости по оси X и Y
        self.speed_y = 0
        self.MAX_SPEED = 400 # максимальная скорость спрайта
        self.on_ground = False # переменная-флаг для отслеживания касатся ли спрайт платформы
        # переменная для отслеживания времени нанесения урона спрайту
        self.time_damaged = -100

    def update_movements(self): # метод для движения спрайта
        if abs(self.speed_x) < 30:
            self.speed_x = 0
        if abs(self.speed_x) >= self.MAX_SPEED:
            if self.speed_x < 0:
                self.speed_x = -self.MAX_SPEED
            else:
                self.speed_x = self.MAX_SPEED
        self.speed_y += 1800 / self.game.fps # скорость спрайта с учетом fps

        self.on_ground = False
        self.x += self.speed_x / self.game.fps # Учитывается fps
        self.y += self.speed_y / self.game.fps
        self.rect.x = self.x
        self.rect.y = self.y

        if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]): # Проверка на столкновение с платформами
            self.y -= self.speed_y / self.game.fps
            self.rect.y = self.y
            # print('x')
            if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]):
                self.x -= self.speed_x / self.game.fps
                self.y += self.speed_y / self.game.fps
                self.rect.x = self.x
                self.rect.y = self.y
                if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]):
                    self.y -= self.speed_y / self.game.fps
                    self.rect.y = self.y
                    if self.speed_y > 0:
                        self.speed_y = 0
                        self.on_ground = True
                    else:
                        self.speed_y = -self.speed_y // 2
            else:
                if self.speed_y > 0:
                    self.speed_y = 0
                    self.on_ground = True
                else:
                    self.speed_y = -self.speed_y // 2
        self.speed_x *= 0.96

    def damage(self, k):
        self.health -= k
        if self.health <= 0:
            self.is_live = False


class EnemyBase(Mob): # наследование от Mob
    def __init__(self, game, pos, health, image):
        super().__init__(game, pos, health, image, game.enemies)
        self.flag = False # флаг для отслеживания касался ли спрайт игрока

    def update_damage(self, k=2):
        if pg.sprite.collide_mask(self, self.game.player):
            if not self.flag:
                self.flag = True
                self.game.player.damage(k)
        else:
            self.flag = False


class Enemy(EnemyBase): # наследование от EnemyBase
    def __init__(self, game, pos, patrol_dist=400):
        self.patrol_dist = patrol_dist
        self.start_x = pos[0]
        im = pg.surface.Surface((100, 140))
        im.fill('green')
        super().__init__(game, pos, 10, im)
        self.speed = 100

    def update(self):
        if time.time() - self.time_damaged > 0.1:  # Если время анимации нанесения урона спрайту вышло
            self.image = pg.image.load('data/enemy.png').convert_alpha()  # Восстанавливаем изображение спрайта
        self.update_movements()
        self.update_damage()
        if not self.is_live:
            self.kill()
            return

        self.speed_x = self.speed
        if self.x - self.start_x > self.patrol_dist:
            if self.speed > 0:
                self.speed = -self.speed
        elif self.x - self.start_x < 0:
            if self.speed < 0:
                self.speed = -self.speed

    def damage(self, k):
        self.game.sound.play('damage')  # Проигрывание звука нанесения урона
        self.time_damaged = time.time()
        self.image = pg.image.load('data/enemy_damaged.png').convert_alpha()
        self.health -= k
        if self.health <= 0:
            self.is_live = False


class Spike(EnemyBase): # наследование от EnemyBase
    def __init__(self, game, pos):
        im = pg.image.load('data/spike.png').convert_alpha()  # Загрузка изображения спрайта
        super().__init__(game, pos, 10 ** 10, im)

    def update(self):
        self.update_damage(10)
