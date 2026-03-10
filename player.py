import pygame


class player:
    def __init__(self, color, rect, xvel=0):
        self.rect = rect
        self.color = color
        self.xvel = xvel
    
    def move(self, drag):
        self.xvel *= drag
        self.rect.x += self.xvel
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=0, border_radius=2)
    