import numpy as np
import pygame


class Obstacle:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.pos = np.array([x, y])
        self.color = (0, 0, 0)
        self.w = w
        self.h = h

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color,
                           (self.pos[0], self.pos[1]), self.w)
