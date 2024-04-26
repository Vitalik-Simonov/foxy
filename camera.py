import pygame as pg
from settings import *
from math import *


class Camera:
    def __init__(self, game, target):
        self.game = game
        self.target = target
        self.x = target.rect.x# - WIDTH // 2
        self.y = target.rect.centery# - HEIGHT // 2
        self.is_move = False
        self.speed = 0
        self.angle = 0

    def update(self):
        if not self.target.groups():
            self.move(self.game.player, 600)
        if self.is_move:
            x = self.new_target.rect.x - self.x
            y = self.new_target.rect.centery - self.y
            try:
                if y < 0:
                    self.angle = 360 - degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
                else:
                    self.angle = degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
            except:
                pass

            self.x += self.speed * cos(radians(self.angle)) / self.game.fps
            self.y += self.speed * sin(radians(self.angle)) / self.game.fps
            if (self.x - self.new_target.rect.x) ** 2 + (self.y - self.new_target.rect.centery) ** 2 <= 10 * self.speed / self.game.fps:
                self.is_move = False
                self.target = self.new_target
                self.x = self.target.rect.x# - WIDTH // 2
                self.y = self.target.rect.centery# - HEIGHT // 2
        else:
            self.x = self.target.rect.x# - WIDTH // 2
            self.y = self.target.rect.centery# - HEIGHT // 2

    def move(self, new_target, speed=100):
        self.speed = speed
        self.new_target = new_target
        self.is_move = True
        x = self.new_target.rect.x - self.x
        y = self.new_target.rect.centery - self.y
        try:
            if y < 0:
                self.angle = 360 - degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
            else:
                self.angle = degrees(acos(x / (x ** 2 + y ** 2) ** 0.5))
        except:
            pass
