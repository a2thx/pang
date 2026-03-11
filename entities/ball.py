import pygame
from config import ballsplityvel, ballsplitxvel, ballminsize
class ball:
    global balls
    balls = []
    def __init__(self, center, radius, color, posx, posy, bounce=1.1, gravity=500, bottombounce=1.21):
        self.center = center
        self.bottombounce = bottombounce
        self.radius = radius
        self.color = color
        self.gravity = gravity
        self.pos = pygame.Vector2(posx, posy)
        self.vel = pygame.Vector2(0, 0)
        self.gr = pygame.Vector2(0, gravity)
        self.bounce = bounce
        self.hitbox = pygame.Rect(posx - radius, posy - radius, radius*2, radius*2)
    
    def move(self, screen, dt, drag=0.99):
        self.pos += self.vel * dt
        self.vel += self.gr * dt
        self.vel.y *= drag
        if self.pos.x - self.radius < 0: #left
            self.pos.x = self.radius
            self.vel.x *= -1
            self.vel.x *= self.bounce #right
        if self.pos.x + self.radius > screen.get_width():
            self.pos.x = screen.get_width() - self.radius
            self.vel.x *= -1
            self.vel.x *= self.bounce
        if self.pos.y - self.radius < 0: #top 
            self.pos.y = self.radius
        if self.pos.y + self.radius > screen.get_height():
            self.pos.y = screen.get_height() - self.radius
            self.vel.y *= -1
            self.vel.y *= self.bottombounce
            
        self.center = (int(self.pos.x), int(self.pos.y))
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), int(self.radius*2), int(self.radius*2))
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def split(self):
        if self.radius > ballminsize:
            self.radius = self.radius // 1.2
            self.vel.y *= -1
            self.vel.y -= self.gravity //2
            self.vel.x -= ballsplitxvel
            b = ball(self.center, self.radius, self.color, self.pos.x, self.pos.y, self.bounce, self.gravity)
            b.vel.y *= -1
            b.vel.y -= self.gravity // 2
            b.vel.x += ballsplityvel
            balls.append(b)
            self.hitbox = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius*2, self.radius*2)
        else:
            balls.remove(self)