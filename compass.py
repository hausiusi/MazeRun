import pygame
import pygame as pg
import math


class Compass:
    def __init__(self, x, y, radius, screen):
        self.font = pg.font.SysFont(None, 30)
        self.radius = radius
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self, angle):
        # draw compass circle edge line
        pg.draw.circle(self.screen, 'black', (self.x, self.y), self.radius, 2)

        pg.draw.circle(self.screen, (128, 128, 128, 128), (self.x, self.y), self.radius - 2)

        # Compass directions
        directions = [('N', 0.5 * math.pi), ('E', math.pi), ('S', 1.5 * math.pi), ('W', 2 * math.pi)]

        # Draw directional markers
        for dir_text, dir_angle in directions:
            rad_angle = dir_angle - angle
            text_x = self.x + math.cos(rad_angle) * (self.radius - 20)
            text_y = self.y - math.sin(rad_angle) * (self.radius - 20)
            text_surface = self.font.render(dir_text, True, 'black')
            self.screen.blit(text_surface,
                             (text_x - text_surface.get_width() // 2, text_y - text_surface.get_height() // 2))

        # Draw the needle (for example, always pointing north)
        needle_length = self.radius - (self.radius // 5)
        needle_north_x = self.x
        needle_north_y = self.y - needle_length
        needle_center_x1 = self.x - (self.radius // 10)
        needle_center_y1 = self.y
        needle_center_x2 = self.x + (self.radius // 10)
        needle_center_y2 = self.y
        needle_south_x = self.x
        needle_south_y = self.y + needle_length
        needle_points_north = [(needle_north_x, needle_north_y),
                               (needle_center_x1, needle_center_y1),
                               (needle_center_x2, needle_center_y2)]
        needle_points_south = [(needle_south_x, needle_south_y),
                               (needle_center_x1, needle_center_y1),
                               (needle_center_x2, needle_center_y2)]

        pg.draw.polygon(self.screen, 'red', needle_points_north, width=3)
        pg.draw.polygon(self.screen, 'orange', needle_points_south)
