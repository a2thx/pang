import pygame
import config as config
from ball import ball, balls
from shot import projectile, projectiles, projectilesdur
from player import player




pygame.init()
screen = pygame.display.set_mode((config.screenwidth, config.screenheight))
clock = pygame.time.Clock()
running = True
dt = 0

paused = False
beaten = False

font = pygame.font.Font(None, size=30)
font2 = pygame.font.Font(None, size=50)

_ball = ball((140, 160), 6, "red", 10, 10, 1, 600)
_ball.vel.x += 180
_ball.vel.y += 50
balls.append(_ball)

playerposdata = pygame.Rect(screen.get_width() // 2, screen.get_height() - config.playerysize, config.playerxsize, config.playerysize)
player = player("white", playerposdata, config.playervel)
hitbox = player.rect

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                if paused or beaten:
                    paused = False
                    beaten = False
                else:
                    projectiles.append(projectile(player.rect))
                    projectilesdur.append(config.prdurationF)
                
    screen.fill("black")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.xvel -= config.addplayervel
    if keys[pygame.K_d]:
        player.xvel += config.addplayervel

    if not paused:
        if len(balls) <=  0:
            beaten = True
        
        for bal in balls:
            bal.move(screen, dt)
            bal.hitbox.clamp_ip(screen.get_rect())
            bal.draw(screen)
            if bal.hitbox.colliderect(player.rect):
                paused = True
            for i in range(len(projectiles) - 1, -1, -1): 
                p = projectiles[i]
                if bal.hitbox.colliderect(p.hitbox):
                    projectiles.pop(i)
                    p.draw(screen)
                    projectilesdur.pop(i)
                    bal.split()
        
        for i in range(len(projectilesdur) - 1, -1, -1):
            projectilesdur[i] -= 1
            if projectilesdur[i] <= 0:
                projectilesdur.pop(i)
                projectiles.pop(i)
                
        for pr in projectiles:
            pr.draw(screen)

                
        player.move(config.grdrag) 
        player.rect.clamp_ip(screen.get_rect())
    player.draw(screen)
    ballstext = font.render("Balls: " + str(len(balls)), True, "white")
    screen.blit(ballstext, (20, 20))
    if paused:
        gameovertext = font2.render("GAME OVER", True, "white")
        gameovertext2 = font.render("press SPACE to restart", True, "white")
        screen.blit(gameovertext, (screen.get_width() // 2 - 100, screen.get_height() // 2))
        screen.blit(gameovertext2, (screen.get_width() // 2 - 105, screen.get_height() // 2 + gameovertext.get_height() + 5))
        balls.clear()
        projectiles.clear()
        projectilesdur.clear()
        _ball = ball((140, 160), 10, "red", 10, 10, 1, 600)
        _ball.vel.x += 180
        _ball.vel.y += 50
        balls.append(_ball)
    if beaten:
        gameovertext = font2.render("LEVEL BEATEN", True, "white")
        gameovertext2 = font.render("press SPACE to restart", True, "white")
        screen.blit(gameovertext, (screen.get_width() // 2 - 100, screen.get_height() // 2))
        screen.blit(gameovertext2, (screen.get_width() // 2 - 105, screen.get_height() // 2 + gameovertext.get_height() + 5))
        balls.clear()
        projectiles.clear()
        projectilesdur.clear()
        _ball = ball((140, 160), 10, "red", 10, 10, 1, 600)
        _ball.vel.x += 180
        _ball.vel.y += 50
        balls.append(_ball)
    pygame.display.flip() 
    dt = clock.tick(60) / 1000


pygame.quit()





