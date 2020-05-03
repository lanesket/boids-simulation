from Boid import Boid
from Obstacle import Obstacle
import pygame
import random
import numpy as np

pygame.init()
pygame.font.init()
width, height = 1280, 720
pygame.display.set_caption('Boids')
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Times New Roman', 18)
white = (255, 255, 255)

clock = pygame.time.Clock()

boids = [Boid(random.randint(0, 1280), random.randint(0, 720), 10, 10)
         for _ in range(30)]
obstacles = []
running = True

is_wind = False
wind_deviation = np.random.randint(-1, 1, 2)

while running:
    screen.fill(white)
    for b in boids:
        b.edges()
        b.flock(boids, obstacles)
        if is_wind:
            b.wind_effect(wind_deviation)
        b.update()
        b.draw(screen)

    for o in obstacles:
        o.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                is_wind = not is_wind
                wind_deviation = np.random.randint(-1, 1, 2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            obstacles.append(Obstacle(pos[0], pos[1], 10, 10))

    clock.tick(60)
    text = font.render(f"Random Wind: {is_wind}", True, (0, 0, 0))
    screen.blit(text, (width - 0.15 * width, 0.1 * height))
    pygame.display.update()

pygame.quit()
