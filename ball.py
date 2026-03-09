import pygame

class ball:
    def __init__(self, center, radius, color, posx, posy, bounce=0.80, gravity=500):
        self.center = center
        self.radius = radius
        self.color = color
        self.pos = pygame.Vector2(posx, posy)
        self.vel = pygame.Vector2(0, 0)
        self.gr = pygame.Vector2(0, gravity)
        self.bounce = bounce
        self.hitbox = pygame.Rect(posx - radius, posy - radius, radius*2, radius*2)
    
    def move(self, screen, dt, drag=0.99):
        self.pos += self.vel * dt
        self.vel += self.gr * dt
        self.vel *= drag
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -1
            self.vel.x *= self.bounce
        if self.pos.x + self.radius > screen.get_width():
            self.pos.x = screen.get_width() - self.radius
            self.vel.x *= -1
            self.vel.x *= self.bounce
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -1
            self.vel.y *= self.bounce
        if self.pos.y + self.radius > screen.get_height():
            self.pos.y = screen.get_height() - self.radius
            self.vel.y *= -1
            self.vel.y *= self.bounce
        self.center = (int(self.pos.x), int(self.pos.y))
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), int(self.radius*2), int(self.radius*2))
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
