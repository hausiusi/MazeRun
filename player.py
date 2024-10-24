from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = game.map.entrance_pos
        self.x += 0.5
        self.y += 0.5
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.level_complete = False

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos

        prev_x, prev_y = self.x, self.y
        self.check_wall_collision(dx, dy)
        if self.x != prev_x or self.y != prev_y:
            if not self.game.sound.steps_channel.get_busy():
                self.game.sound.steps.play()

        exit_pos = self.game.map.exit_pos
        if exit_pos[0] - 0.5 < self.x < exit_pos[0] + 0.5 and exit_pos[1] - 0.5 < self.y < exit_pos[1] + 0.5:
            if not self.level_complete:
                self.game.sound.level_complete.play()
                self.level_complete = True

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self, force_2_d: bool):
        if force_2_d:
            pg.draw.line(self.game.screen, "yellow", (self.x * 100, self.y * 100),
                         (self.x * 100 + WIDTH * math.cos(self.angle),
                         self.y * 100 + WIDTH * math.sin(self.angle)), 2)

        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.hand.reloading:
                self.shot = True
                self.game.hand.reloading = True
