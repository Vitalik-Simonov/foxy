from settings import *
from math import sqrt


class Button(pg.sprite.Sprite):
    def __init__(self, game, im, x, y, *groups):
        super(Button, self).__init__(*groups)
        self.game = game
        self.image = pg.image.load(im).convert_alpha() # загрузка изображения
        self.rect = self.image.get_rect() # создание хитбокса
        self.rect.x = x # координаты хитбокса
        self.rect.y = y

    def pressed(self): # проверка нажатия
        mouse = pg.mouse.get_pos()
        if mouse[0] >= self.rect.topleft[0]:
            if mouse[1] >= self.rect.topleft[1]:
                if mouse[0] <= self.rect.bottomright[0]:
                    if mouse[1] <= self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


class Pause(Button):
    def __init__(self, game):
        super(Pause, self).__init__(game, 'data/pause.png', 15, 10, game.ui)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            d = PauseMenu(self.game)
            del d


class SoundOnOff(Button):
    def __init__(self, game):
        super(SoundOnOff, self).__init__(game, 'data/sound_off.png', 15, 75, game.ui)
        self.game = game
        self.volume = self.game.sound.music.get_volume()
        self.is_pressed = True

    def update(self):
        if self.game.sound.music.get_volume() > 0.01:
            self.volume = self.game.sound.music.get_volume()
        if not pg.mouse.get_pressed(3)[0]:
            self.is_pressed = True
        if pg.mouse.get_pressed(3)[0] and self.pressed() and self.is_pressed:
            self.is_pressed = False
            if self.game.sound.music.get_volume() > 0.01:
                self.game.sound.set_volume(0)
                self.image = pg.image.load('data/sound_on.png').convert_alpha()
            else:
                self.game.sound.set_volume(self.volume)
                self.image = pg.image.load('data/sound_off.png').convert_alpha()


class Play(Button):
    def __init__(self, game):
        super(Play, self).__init__(game, 'data/play.png', 500, 450)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            return True


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.play = Play(self.game)
        self.slider = Slider(self.game, 'black', 'red', 1000, 700, 450, 100, self.game.sound.music.get_volume())
        self.run()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def run(self):
        while True:
            self.game.screen.fill((60, 10, 150))
            self.check_events()
            self.game.screen.blit(self.play.image, self.play.rect)
            if self.game.sound.music.get_volume() > 0.01:
                self.slider.update()
            self.game.screen.blit(self.slider.image, self.slider.rect)
            if self.play.update():
                del self.play
                break
            self.game.sound.set_volume(self.slider.value)
            pg.display.flip()
            self.game.clock.tick(FPS)


class Slider(pg.sprite.Sprite):
    def __init__(self, game, color1, color2, x, y, l, w, value, *groups):
        super(Slider, self).__init__(*groups)
        self.game = game
        self.image = pg.surface.Surface((w, l)) # создание изображения
        self.rect = self.image.get_rect() # создание хитбокса
        self.rect.x = x
        self.rect.bottom = y
        self.color1 = color1 # цвет слайдера
        self.color2 = color2
        self.l = l # длина
        self.w = w # ширина
        self.value = value # текущее значение

    def pressed(self): # проверка нажатия
        mouse = pg.mouse.get_pos()
        if mouse[0] >= self.rect.topleft[0]:
            if mouse[1] >= self.rect.topleft[1]:
                if mouse[0] <= self.rect.bottomright[0]:
                    if mouse[1] <= self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def update(self):
        if self.pressed():
            y = pg.mouse.get_pos()[1]
            self.value = abs(y - self.rect.bottom) / self.l
        self.image.fill(self.color2)
        pg.draw.rect(self.image, self.color1, (0, 0, self.w, self.l - self.value * self.l))


class Start(Button):
    def __init__(self, game):
        im = pg.image.load('data/play.png')
        super(Start, self).__init__(game, 'data/play.png', WIDTH // 2 - im.get_width() // 2, HEIGHT // 2 - im.get_height() // 2)
        self.game = game

    def update(self):
        if pg.mouse.get_pressed(3)[0] and self.pressed():
            return True


class StartMenu:
    def __init__(self, game):
        self.game = game
        self.play = Start(self.game)
        self.slider = Slider(self.game, 'black', 'red', 1200, 1000, 450, 100, pg.mixer.music.get_volume())
        self.run()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def run(self):
        while True:
            self.game.screen.fill((60, 10, 150))
            self.check_events()
            self.game.screen.blit(pg.image.load('data/bg_start.png'), (0, 0))
            self.game.screen.blit(self.play.image, self.play.rect)
            if self.game.sound.music.get_volume() > 0.01:
                self.slider.update()
            self.game.screen.blit(self.slider.image, self.slider.rect)
            if self.play.update():
                del self.play
                break
            self.game.sound.set_volume(self.slider.value)
            pg.display.flip()
            self.game.clock.tick(FPS)
