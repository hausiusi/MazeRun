from sprite_object import *
import random


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = "resources/sprites/static_sprites/"
        self.anim_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self.add_sprite

    def randomize_sprite_positions(self, count):
        walkable_positions = []
        for j, row in enumerate(self.game.map.mini_map):
            for i, value in enumerate(row):
                if not value:
                    walkable_positions.append((i+0.2, j+0.2))

        random.shuffle(walkable_positions)
        for i in range(count):
            self.add_sprite(AnimatedSprite(self.game, pos=walkable_positions[i]))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
