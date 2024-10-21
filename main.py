#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from hand import *
from compass import *
from live_map import *
from sound import *


class Game:
    def __init__(self, force_2d=False):
        self.sound = None
        self.compass = None
        self.live_map = None
        self.hand = None
        self.object_handler = None
        self.animated_sprite = None
        self.static_sprite = None
        self.object_renderer = None
        self.raycasting = None
        self.player = None
        self.map = None
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.force_2_d = force_2d

    def new_game(self):
        self.map = Map(self, 15, 15)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)
        self.animated_sprite = AnimatedSprite(self)
        self.object_handler = ObjectHandler(self)
        self.hand = Hand(self)
        self.live_map = LiveMap(self)
        compass_x = self.hand.weapon_pos[0] + 300
        compass_y = self.hand.weapon_pos[1] + 110
        self.compass = Compass(compass_x, compass_y, 70, self.screen)
        self.sound = Sound(self)
        self.object_handler.randomize_sprite_positions(15)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.hand.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps() : .1f}FPS. POS:{self.player.pos}")

    def draw(self):
        # self.screen.fill("black")
        if not self.force_2_d:
            self.object_renderer.draw()
            self.hand.draw()
            self.compass.draw(self.player.angle + (0.5 * math.pi))
            self.live_map.draw(WIDTH / 7, WIDTH / 7, (20, 20))
            self.live_map.update()
        else:
            self.map.draw()
            self.player.draw(self.force_2_d)
            self.compass.draw(self.player.angle + + (0.5 * math.pi))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.player.single_fire_event(event)

    def run(self):
        self.sound.theme.play()
        self.sound.play_background_music()
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game(False)
    game.run()
