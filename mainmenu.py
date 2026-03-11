from pyplus import BUTTON, LABEL, container, pyplusINIT
import pygame
from enum import Enum, auto
menu_action = None

class state(Enum):
    PLAY = auto()
    OPTIONS = auto()
    QUIT = auto()


def play():
    global action
    action = state.PLAY


def options():
    global action
    action = state.OPTIONS


def quit():
    global action
    action = state.QUIT


pygame.init()
font = pygame.font.Font(None, 36)
pangfont = pygame.font.Font(None, 50)
play_ = BUTTON(font=font, pos=pygame.Vector2(100, 50), text="Play", color=(100, 200, 100), cornerradius=8, onclick=play)
play_.hovercolor = (120, 220, 120)
play_.clickcolor = (0, 150, 0)
play_.hoversize = 1.1

options_ = BUTTON(font=font, pos=pygame.Vector2(100, 120), text="Options", color=(200, 200, 100), cornerradius=8, onclick=options)
options_.hovercolor = (220, 220, 120)
options_.hoversize = 1.1
options_.clickcolor = (150, 150, 0)

quit_ = BUTTON(font=font, pos=pygame.Vector2(100, 190), text="Quit", color=(200, 100, 100), cornerradius=8, onclick=quit)
quit_.hovercolor = (220, 120, 120)
quit_.hoversize = 1.1
quit_.clickcolor = (150, 0, 0)
play_.rect.size = (150, 64)
quit_.rect.size = (150, 64)
options_.rect.size = (150, 64)

panglabel = LABEL(font=pangfont, pos=pygame.Vector2(100, 100), text="PANG", color=None)
_container = container(display=container.DISPLAY.VERTICAL, allignitems=container.ALIGNITEMS.CENTER, size=(1080, 720), pos=pygame.Vector2(0, 0))
_container.add(panglabel)
_container.add(play_)
_container.add(options_)
_container.add(quit_)
_container.pack()


def mainmenu(screen):
    global action
    action = None
    clock = pygame.time.Clock()
    while action is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = state.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = state.PLAY

        screen.fill("black")
        pyplusINIT(screen)
        pygame.display.flip()
        clock.tick(60)
    return action
