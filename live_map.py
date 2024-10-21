import pygame as pg


class LiveMap:
    def __init__(self, game):
        self.game = game

    def draw(self, width, height, pos=(0, 0)):
        self.pos = pos
        self.rect_width = width // self.game.map.width
        self.rect_height = height // self.game.map.height
        [pg.draw.rect(self.game.screen,
                      (50, 50, 50),
                      (pos[0] + p[0] * self.rect_width, pos[1] + p[1] * self.rect_height, self.rect_width, self.rect_height))
         for p in self.game.map.world_map]

        # mark entrance and exit
        entrance_pos = (pos[0] + self.game.map.entrance_pos[0] * self.rect_width,
                        pos[1] + self.game.map.entrance_pos[1] * self.rect_height)
        pg.draw.rect(self.game.screen, "red", (entrance_pos[0], entrance_pos[1], self.rect_width, self.rect_height))
        exit_pos = (pos[0] + self.game.map.exit_pos[0] * self.rect_width,
                    pos[1] + self.game.map.exit_pos[1] * self.rect_height)
        pg.draw.rect(self.game.screen, "blue", (exit_pos[0], exit_pos[1], self.rect_width, self.rect_height))

    def update(self):
        pos = (self.pos[0] + self.rect_width * self.game.player.x, self.pos[1] + self.rect_height * self.game.player.y)
        pg.draw.circle(self.game.screen, 'green', pos, self.rect_width // 2)
