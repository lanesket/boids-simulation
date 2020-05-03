from typing import List
import numpy as np
import random
import pygame
import math


def distance(p1: np.ndarray, p2: np.ndarray) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


class Boid:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.pos = np.array([x, y]).astype(float)
        self.w = w
        self.h = h
        self.velocity = (np.random.rand(2)) * 10
        self.acceleration = (np.random.rand(2))
        self.max_speed = 5
        self.max_force = 0.2
        self.perception = 50

    def edges(self, scr_w=1280, scr_h=720) -> None:
        if self.pos[0] > scr_w:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = scr_w

        if self.pos[1] > scr_h:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = scr_h

    def update(self) -> None:
        """
            Update per frame
        """
        self.pos += self.velocity
        self.velocity += self.acceleration

        # Limits the speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / \
                np.linalg.norm(self.velocity) * self.max_speed

    def alignment(self, boids: List) -> np.ndarray:
        """
            The alignment rule of the flock
        """
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for b in boids:
            if b != self and (distance(self.pos, b.pos) < self.perception):
                total += 1
                avg += b.velocity
        if total:
            avg /= total
            # normilizing the vector for getting direction
            avg = (avg / np.linalg.norm(avg)) * self.max_speed
            steering_force = avg - self.velocity

        return steering_force

    def cohesion(self, boids: List) -> np.ndarray:
        """
            The cohesion rule of the flock
        """
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for b in boids:
            if b != self and (distance(self.pos, b.pos) < self.perception):
                total += 1
                avg += b.pos
        if total:
            mass_center = avg / total
            steering_force = mass_center - self.pos

            if np.linalg.norm(steering_force) > 0:
                steering_force = (
                    steering_force / np.linalg.norm(steering_force)) * self.max_speed

            steering_force -= self.velocity
            if np.linalg.norm(steering_force) > self.max_force:
                steering_force = (
                    steering_force / np.linalg.norm(steering_force)) * self.max_force

        return steering_force

    def separation(self, boids: List) -> np.ndarray:
        """
            The separation rule of the flock
        """
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for b in boids:
            dist = np.linalg.norm(self.pos - b.pos)
            # dist = distance(self.pos, b.pos)
            if b != self and (dist < self.perception):
                diff = self.pos - b.pos
                diff /= dist
                total += 1
                avg += diff

        if total:
            avg /= total
            steering_force = avg
            if np.linalg.norm(steering_force) > 0:
                steering_force = (
                    steering_force / np.linalg.norm(steering_force)) * self.max_speed

            steering_force -= self.velocity
            if np.linalg.norm(steering_force) > self.max_force:
                steering_force = (
                    steering_force / np.linalg.norm(steering_force)) * (self.max_force + 0.1)

        return steering_force

    def flock(self, boids: List):
        """
            Applies all the flock rules
        """
        self.acceleration = np.zeros(2).astype(float)

        alignment = self.alignment(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.pos[0], self.pos[1], self.w, self.h))
