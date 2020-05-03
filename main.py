from Boid import Boid
import pygame
import random


pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
white = (255, 255, 255)

clock = pygame.time.Clock()

boids = [Boid(random.randint(0, 1280), random.randint(0, 720), 10, 10) for _ in range(30)]
running = True

while running:
    screen.fill(white)
    for b in boids:
        b.edges()
        b.flock(boids)
        b.update()
        b.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)
    pygame.display.update()

pygame.quit()