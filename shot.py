import pygame
from config import prheight, prwitdth, prdurationF

class projectile:
    global projectiles, projectilesdur
    projectiles = []
    projectilesdur = []
    def __init__(self, pos, color="yellow",width=prwitdth, height=prheight, duritation=prdurationF):
        self.color = color
        self.duritation = duritation
        self.width = width
        self.height = height
        self.pos = pygame.Vector2(pos.x + pos.w // 2, 0) 
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, width, height)
    
    def draw(self, screen):
        self.hitbox.topleft = (self.pos.x, self.pos.y) 
        pygame.draw.rect(screen, self.color, self.hitbox, border_radius=1)
    