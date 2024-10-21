import pygame as pg
import random

from settings import *

_ = False


class Map:
    def __init__(self, game, width, height):
        self.exit_pos = (0, 0)
        self.entrance_pos = (0, 0)
        self.game = game
        self.mini_map = []
        self.width = width
        self.height = height
        self._generate()  # mini_map
        print(self.mini_map)
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        rect_width = WIDTH // self.width
        rect_height = HEIGHT // self.height
        [pg.draw.rect(self.game.screen,
                      "darkgray",
                      (p[0] * rect_width, p[1] * rect_height, rect_width, rect_height), 2)
         for p in self.world_map]

    def _generate(self, texture_chance=0.3):
        # Initialize the map with walls (1)
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Function to check if a position is valid to carve a path
        def is_valid(x, y):
            if x < 1 or x >= self.width - 1 or y < 1 or y >= self.height - 1:
                return False
            if maze[y][x] == 0:
                return False
            surrounding_walls = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if maze[y + dy][x + dx] == 1:
                    surrounding_walls += 1
            return surrounding_walls >= 3  # carve only if mostly surrounded by walls

        # Depth-First Search to carve paths
        def carve_path(x, y):
            maze[y][x] = 0  # Carve the path
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_valid(new_x, new_y):
                    carve_path(new_x, new_y)

        # Start carving the maze from a random odd position
        start_x, start_y = random.randrange(1, self.width - 1, 2), random.randrange(1, self.height - 1, 2)
        carve_path(start_x, start_y)

        # Add entrance (at top) and exit (at bottom)
        entrance_x = random.randrange(1, self.width - 1, 2)  # Ensure entrance is at an odd index for balance
        exit_x = random.randrange(1, self.width - 1, 2)  # Ensure exit is at an odd index for balance
        maze[0][entrance_x] = -1  # Entrance at the top wall
        maze[self.height - 1][exit_x] = -2  # Exit at the bottom wall
        self.entrance_pos = (entrance_x, 1)
        self.exit_pos = (exit_x, self.height - 1)

        # Add random textures (2, 3, 4) to walls
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if maze[y][x] == 1 and random.random() < texture_chance:
                    maze[y][x] = random.choice([2, 3, 4])

        self.mini_map = maze
