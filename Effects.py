import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x_pos,  y_pos, screen):
        super().__init__()
        self.image = pygame.Surface((1, 1)).convert_alpha()
        self.radius = 20
        self.width =20
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen


        self.rect = self.image.get_rect()
    def update(self):
        pygame.draw.circle(self.screen, (255,255,255),(self.x_pos, self.y_pos), self.radius,self.width)
        self.radius +=20
        if self.width <= 1:
            self.width = 1
        else: self.width-=2
        if self.radius >= 200:
            self.kill()


