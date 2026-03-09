import pygame
from ball import ball
from player import player

#settings
addplayervel = 3
playervel = 0
playerxsize = 40
playerysize = 60
grdrag = 0.80
airdrag = 0.97

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

_ball = ball((640, 360), 15, "red", 640, 360, 0.80, 500)


playerposdata = pygame.Rect(screen.get_width() // 2, screen.get_height() - playerysize, playerxsize, playerysize)
player = player("red", playerposdata, playervel)
hitbox = player.rect

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("black")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.xvel -= addplayervel
    if keys[pygame.K_d]:
        player.xvel += addplayervel
    player.move(grdrag)
    _ball.move(screen, dt)
    _ball.hitbox.clamp_ip(screen.get_rect())
    _ball.draw(screen)
    player.rect.clamp_ip(screen.get_rect())
    player.draw(screen)
    #ball1.updatepos(dt)
    #ball1.draw(screen)
    
    pygame.display.flip() 
    dt = clock.tick(60) / 1000


pygame.quit()





