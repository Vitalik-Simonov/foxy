import pygame as pg
from settings import *
from sound import *
from player import *
from level import *
from gun import *
from camera import *
from mobs import *
from time import *
import os
import sys
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
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = load_platforms(self)
        Gun(self, self.player)
        self.camera = Camera(self, self.player)
        self.sound = Sound()
        Enemy(self, (WIDTH // 4 - 350, 825))

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
        self.all_sprites.update()
        self.camera.update()

    def draw(self):
        self.screen2.fill((100, 100, 100))
        self.all_sprites.draw(self.screen2)
        score_text = font.render("Счёт: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()  # создание хитбокса текста
        score_rect.topleft = (50, 50)
        self.screen.fill('black')
        self.screen.blit(self.screen2, (-self.camera.x + WIDTH // 2, -self.camera.y + HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        # print(-self.camera.x + WIDTH // 2, -self.camera.y + HEIGHT // 2)

    def run(self):
        self.running = True
        while self.running:
            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(60000)
            self.fps = self.clock.get_fps()
            if self.fps == 0:
                self.fps = 60


if __name__ == '__main__':
    app = App()
    app.setup()
    app.run()