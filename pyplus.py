import pygame
from ui import BUTTON, LABEL, container


def pyplusINIT(screen):
    mousepos = pygame.mouse.get_pos()
    mousepressed = pygame.mouse.get_pressed()
    
    for button in BUTTON.buttonslist:
        if button.rect.collidepoint(mousepos):
            if mousepressed[0]:
                if button.state != BUTTON.STATE.CLICKED:
                    button.state = BUTTON.STATE.CLICKED
                    if button.onclick:
                        button.onclick()
            elif button.state != BUTTON.STATE.HOVER:
                button.state = BUTTON.STATE.HOVER
        elif button.state != BUTTON.STATE.DEFAULT:
            button.state = BUTTON.STATE.DEFAULT
            
    for button in BUTTON.buttonslist:
        if button.rect.collidepoint(mousepos):
            if mousepressed[0]:
                button.state = BUTTON.STATE.CLICKED
            else:
                button.state = BUTTON.STATE.HOVER
        else:
            button.state = BUTTON.STATE.DEFAULT
        if button.state == BUTTON.STATE.CLICKED and mousepressed[0]:
            if button.onclick:
                button.onclick()
    for button in BUTTON.buttonslist:
        button.draw(screen)
        
    for label in LABEL.labellist:
        if label.rect.collidepoint(mousepos):
            label.state = LABEL.STATE.HOVER
        else:
            label.state = LABEL.STATE.DEFAULT
    for label in LABEL.labellist:
        label.draw(screen)
    
    for cont in container.containerlist:
        for child in cont.packedlist:
            child.draw(screen)
