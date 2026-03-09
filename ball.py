import pygame

class ball:
    def __init__(self, size, xpos, ypos, yvel, xvel, color, gravity):
        self.size = size
        self.color = color
        self.xpos = xpos
        self.ypos = ypos
        self.yvel = yvel
        self.xvel = xvel
        self.gravity = gravity
        
    def updatepos(self, dt):
        self.yvel = self.yvel + self.gravity * dt
        self.xpos += self.xvel * dt
        self.ypos += self.yvel * dt
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.xpos), int(self.ypos)), self.size)
