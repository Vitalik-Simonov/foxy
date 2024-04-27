import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.music = pg.mixer.Sound('data/music.ogg')  # Инициализация музыки
        self.music.play(-1)  # Повтор музыки

    def stop_music(self):  # Остановка музыки
        self.music.stop()

    def set_volume(self, k):  # Установка громкости
        self.music.set_volume(k)

    def play(self, sound):  # Проигрывание звука
        if self.music.get_volume() > 0.01:  # Если громкость больше 0.01
            pg.mixer.Sound.play(pg.mixer.Sound('data/' + sound + '.ogg'))
