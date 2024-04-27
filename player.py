import pygame as pg
from settings import *
import time


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        super().__init__(game.all_sprites)
        # создание изображения для спрайта
        self.im = pg.image.load('data/player.png').convert_alpha()
        self.image = self.im.copy()
        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)
        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()

        # начальные координаты спрайта
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        # компоненты скорости по оси X и Y
        self.speed_x = 0
        self.speed_y = 0
        self.MAX_SPEED = 400

        # переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False
        # переменная-флаг для отслеживания жив ли спрайт
        self.is_live = True
        # переменная для отслеживания времени нанесения урона спрайту
        self.time_damaged = -100
        # здоровье спрайта
        self.health = 10
        self.direction = 1

    def update(self):
        if self.speed_x > 0:
            self.direction = 1
        elif self.speed_x < 0:
            self.direction = -1
        if time.time() - self.time_damaged > 0.1:  # Если время анимации нанесения урона спрайту вышло
            if self.direction > 0:
                self.direction = 1
                self.image = self.im.copy()  # Восстанавливаем изображение спрайта
            else:
                self.direction = -1
                self.image = pg.transform.flip(self.im.copy(), True, False)
        else:
            if self.speed_x > 0:
                self.image = pg.image.load('data/player_damaged.png').convert_alpha()
            else:
                self.image = pg.transform.flip(pg.image.load('data/player_damaged.png').convert_alpha(), True, False)
        # создание маски для спрайта
        self.mask = pg.mask.from_surface(self.image)
        if not self.is_live or self.y >= MAP_HEIGHT - self.rect.height - 1:  # Если спрайт умер или вышел за пределы экрана
            self.kill()
            self.game.running = False
            return

        # Обновление скоростей спрайта
        if abs(self.speed_x) < 30:
            self.speed_x = 0
        if abs(self.speed_x) >= self.MAX_SPEED:
            if self.speed_x < 0:
                self.speed_x = -self.MAX_SPEED
            else:
                self.speed_x = self.MAX_SPEED
        self.speed_y += 1800 / self.game.fps

        self.on_ground = False
        self.x += self.speed_x / self.game.fps  # Учитывается fps
        self.y += self.speed_y / self.game.fps

        if self.x < 0:  # Если спрайт вышел за пределы экрана
            self.x = 0
        if self.x > MAP_WIDTH - self.rect.width:
            self.x = MAP_WIDTH - self.rect.width
        if self.y < 0:
            self.y = 0
        if self.y > MAP_HEIGHT - self.rect.height:
            self.y = MAP_HEIGHT - self.rect.height

        self.rect.x = self.x
        self.rect.y = self.y

        if any([pg.sprite.collide_mask(self, i) for i in self.game.platforms]):  # Проверка на столкновение с платформами
            self.y -= self.speed_y / self.game.fps  # Учитывается fps
            self.rect.y = self.y
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

        # проверка на нажатие клавиш и управление спрайтом
        if pg.key.get_pressed()[pg.K_w] or pg.key.get_pressed()[pg.K_UP]:
            if self.on_ground:
                self.speed_y = -1000
        if pg.key.get_pressed()[pg.K_s] or pg.key.get_pressed()[pg.K_DOWN]:
            self.speed_y += 30

        if pg.key.get_pressed()[pg.K_a] or pg.key.get_pressed()[pg.K_LEFT]:
            self.speed_x -= 50
        if pg.key.get_pressed()[pg.K_d] or pg.key.get_pressed()[pg.K_RIGHT]:
            self.speed_x += 50

    # функция для уменьшения здоровья
    def damage(self, k):
        self.game.sound.play('damage')  # Проигрывание звука нанесения урона
        self.time_damaged = time.time()
        self.image = pg.image.load('data/player_damaged.png').convert_alpha()
        self.health -= k
        if self.health <= 0:
            self.is_live = False
