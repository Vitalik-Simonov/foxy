import pygame as pg
from settings import *
from ui import *
import asyncio
from sound import *
from player import *
from level import *
from gun import *
from camera import *
from mobs import *
from time import *
import os
import sys
import time
os.chdir('\\'.join(sys.argv[0].split('\\')[:-1]))


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = 60
        self.screen2 = pg.surface.Surface((MAP_WIDTH, MAP_HEIGHT))  # для камеры

    def setup(self):  # инициализация игры
        self.fuel = 0  # количество бензина
        self.gear = 0  # количество шестеренок
        self.box = 0  # количество ящиков
        self.winning = False
        self.all_sprites = pg.sprite.Group()
        self.ui = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.platforms = load_platforms(self)
        self.player = Player(self)
        Gun(self, self.player)
        self.camera = Camera(self, self.player)
        self.sound = Sound()
        Pause(self)
        SoundOnOff(self)

    def delete_all(self):
        self.all_sprites.empty()
        self.ui.empty()
        self.mobs.empty()
        self.enemies.empty()
        self.platforms = []

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        self.all_sprites.update()
        self.ui.update()
        self.camera.update()

    def draw(self):
        self.screen2.fill((100, 100, 100))
        self.all_sprites.draw(self.screen2)
        score_text = font.render(f'Счёт: {str(self.fuel)}      {str(self.gear)}      {str(self.box)}', True, WHITE)
        score_rect = score_text.get_rect()  # создание хитбокса текста
        score_rect.topleft = (100, 20)
        self.screen.fill('black')
        self.screen.blit(self.screen2, (-self.camera.x + WIDTH // 2, -self.camera.y + HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        self.screen.blit(pg.image.load('data/ui.png'), (190, 20))
        self.ui.draw(self.screen)

    async def run(self):
        self.screen.blit(pg.image.load('data/first.png'), (0, 0))
        pg.display.flip()
        run = True
        while run:
            for event in pg.event.get():
                if pg.mouse.get_pressed()[0]:
                    run = False
                    break
                elif event.type == pg.QUIT:
                    exit()
            await asyncio.sleep(0)
        self.screen.blit(pg.image.load('data/instruction.png'), (0, 0))
        pg.display.flip()
        run = True
        while run:
            for event in pg.event.get():
                if pg.mouse.get_pressed()[0]:
                    run = False
                    break
                elif event.type == pg.QUIT:
                    exit()
            await asyncio.sleep(0)
        StartMenu(self)
        self.running = True
        while self.running:
            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
            self.fps = self.clock.get_fps()
            if self.fps == 0:
                self.fps = 60
        if self.winning:
            self.happy_end()
        else:
            self.end()

    def end(self):
        orig_im = pg.image.load('data/anim_bg2.png')
        w, h = orig_im.get_size()
        for i in range(800, 100, -15):
            self.screen.blit(pg.transform.scale(orig_im, (w * i / 199, h * i / 199)), (400 - i * 4, 200 - i * 2))
            pg.display.flip()
        time.sleep(2)

    def happy_end(self):
        self.screen.blit(pg.image.load('data/anim_bg.png'), (0, 0))
        pg.display.flip()
        rocket = AnimatioRocket(self)
        orig_im = pg.image.load('data/rocket_fire.png')
        rocket.rect.right = 900
        rocket.rect.bottom = 577
        w, h = orig_im.get_size()
        h *= 0.054
        w *= 0.054
        for i in range(45):
            self.screen.blit(pg.image.load('data/anim_bg.png'), (0, 0))
            rocket.rect.x -= 1.6
            rocket.rect.y -= 1.6
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(FPS)
            rocket.image = pg.transform.rotate(pg.transform.scale(orig_im, (w, h)), 45 + i)
            x, y = rocket.rect.right, rocket.rect.bottom
            rocket.rect = rocket.image.get_rect()
            rocket.rect.right, rocket.rect.bottom = x, y
            w *= 1.05
            h *= 1.05
        for i in range(200):
            self.screen.blit(pg.image.load('data/anim_bg.png'), (0, 0))
            rocket.rect.x -= 5
            self.screen.blit(rocket.image, rocket.rect)
            pg.display.flip()
            self.clock.tick(FPS)


class AnimatioRocket(pg.sprite.Sprite):
    def __init__(self, game):
        super(AnimatioRocket, self).__init__()
        self.game = game
        self.image = pg.transform.scale(pg.transform.rotate(pg.image.load('data/rocket_fire.png').convert_alpha(), -90),
                                        (pg.image.load('data/rocket_fire.png').get_height() // 2,
                                         pg.image.load('data/rocket_fire.png').get_width() // 2))
        self.rect = self.image.get_rect()
        self.rect.x = -self.image.get_width()
        self.rect.y = HEIGHT // 4

    def update1(self):
        self.rect.x += 5

    def update2(self):
        self.rect.x += 3.6
        self.rect.y += 3.6


if __name__ == '__main__':
    app = App()
    while True:
        app.setup()
        asyncio.run(app.run())
        app.sound.stop_music()
        app.delete_all()
