import pygame as pg


pg.init()

# константы-параметры окна
WIDTH = 1920
HEIGHT = 1080

FPS = 60000

MAP_WIDTH = WIDTH * 3
MAP_HEIGHT = HEIGHT * 3
# константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
font = pg.font.Font(None, 36)
TARGET_FUEL = 5
TARGET_GEAR = 4
TARGET_BOX = 1
