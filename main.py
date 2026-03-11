import pygame
import config as config
from entities.ball import ball, balls
from entities.shot import projectile, projectiles, projectilesdur
from entities.player import player
from mainmenu import mainmenu, state
from enum import Enum, auto


class gamestate(Enum):
    MAINMENU = auto()
    OPTIONSMENU = auto()
    INGAME = auto()
    STARTGAME = auto()
    STOPGAME = auto()
    LOST = auto()
    BEATLEVEL = auto()
    PAUSED = auto()

pygame.init()
screen = pygame.display.set_mode((config.screenwidth, config.screenheight))
clock = pygame.time.Clock()
running = True
dt = 0

paused = False
beaten = False

font = pygame.font.Font(None, size=25)
font2 = pygame.font.Font(None, size=50)

_ball = ball((140, 160), 6, "red", 10, 10, 1, 600)
_ball.vel.x += 180
_ball.vel.y += 50
balls.append(_ball)

playerposdata = pygame.Rect(screen.get_width() // 2, screen.get_height() - config.playerysize, config.playerxsize, config.playerysize)
player = player("white", playerposdata, config.playervel)
hitbox = player.rect
currentgamestate = gamestate.MAINMENU


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                if currentgamestate == gamestate.PAUSED:
                    currentgamestate = gamestate.INGAME
                elif currentgamestate == gamestate.LOST:
                    currentgamestate = gamestate.STOPGAME
                elif currentgamestate == gamestate.BEATLEVEL:
                    currentgamestate = gamestate.STOPGAME
                else:
                    projectiles.append(projectile(player.rect))
                    projectilesdur.append(config.prdurationF)
            if event.key == pygame.K_ESCAPE:
                action = mainmenu(screen)
                if action == state.QUIT:
                    running = False
                elif action == state.OPTIONS:
                    currentgamestate = gamestate.OPTIONSMENU
                
    screen.fill("black")
    match currentgamestate:
        case gamestate.MAINMENU:
            action = mainmenu(screen)
            if action == state.PLAY:
                currentgamestate = gamestate.STARTGAME
            elif action == state.QUIT:
                running = False
            elif action == state.OPTIONS:
                currentgamestate = gamestate.OPTIONSMENU
        case gamestate.OPTIONSMENU:
            currentgamestate = gamestate.MAINMENU #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
        case gamestate.LOST:
            gameovertext = font2.render("GAME OVER", True, "white")
            gameovertext2 = font.render("press SPACE to restart or ESC to go to the main menu", True, "white")
            screen.blit(gameovertext, (screen.get_width() // 2 - gameovertext.get_width() // 2, screen.get_height() // 2))
            screen.blit(gameovertext2, (screen.get_width() // 2 - gameovertext2.get_width() // 2, screen.get_height() // 2 + gameovertext.get_height() + 5))
        case gamestate.PAUSED:
            gameovertext = font2.render("PAUSED", True, "white")
            gameovertext2 = font.render("press SPACE to continue", True, "white")
            screen.blit(gameovertext, (screen.get_width() // 2 - 100, screen.get_height() // 2))
            screen.blit(gameovertext2, (screen.get_width() // 2 - 105, screen.get_height() // 2 + gameovertext.get_height() + 5))
        case gamestate.BEATLEVEL:
            gameovertext = font2.render("LEVEL BEATEN", True, "white")
            gameovertext2 = font.render("press SPACE to restart", True, "white")
            screen.blit(gameovertext, (screen.get_width() // 2 - 100, screen.get_height() // 2))
            screen.blit(gameovertext2, (screen.get_width() // 2 - 105, screen.get_height() // 2 + gameovertext.get_height() + 5))
        case gamestate.STARTGAME:
            balls.clear()
            _ball = ball((140, 160), 6, "red", 10, 10, 1, 600)
            _ball.vel.x += 180
            _ball.vel.y += 50
            balls.append(_ball)
            currentgamestate = gamestate.INGAME
        case gamestate.STOPGAME:
            balls.clear()
            projectiles.clear()
            projectilesdur.clear()
            currentgamestate = gamestate.STARTGAME
        case gamestate.INGAME:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.xvel -= config.addplayervel
            if keys[pygame.K_d]:
                player.xvel += config.addplayervel
            if len(balls) <=  0:
                currentgamestate = gamestate.BEATLEVEL
            for bal in balls:
                bal.move(screen, dt)
                bal.hitbox.clamp_ip(screen.get_rect())
                bal.draw(screen)
                if bal.hitbox.colliderect(player.rect):
                    currentgamestate = gamestate.LOST
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
    pygame.display.flip() 
    dt = clock.tick(60) / 1000


pygame.quit()




