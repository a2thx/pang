import pygame
from ball import ball
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
ball1 = ball(30, 100, 100, 0, 0, "red", 60)
dt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")
    keys = pygame.key.get_pressed()
    # RENDER YOUR GAME HERE
    ball1.updatepos(dt)
    ball1.draw(screen)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

