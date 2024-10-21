import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = "resources/sound/"
        self.background_music_path = self.path + "background.mp3"
        self.theme = pg.mixer.Sound(self.path + "intro.mp3")
        self.steps = pg.mixer.Sound(self.path + "steps.mp3")
        self.level_complete = pg.mixer.Sound(self.path + "level_complete.mp3")
        self.steps.set_volume(0.2)
        self.steps_channel = pg.mixer.find_channel()
        pg.mixer.music.set_volume(0.3)

    def play_background_music(self):
        pg.mixer.music.load(self.background_music_path)
        pg.mixer.music.set_volume(0.4)
        pg.mixer.music.play(loops=-1)
