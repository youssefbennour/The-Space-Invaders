import pygame
class Laser(pygame.sprite.Sprite):
    def __init__(self, type, x,y, speed):
        super().__init__()
        self.type = type
        self.speed= speed
        if type == "yellow":
            self.image = pygame.image.load('assets/pixel_laser_yellow.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft=(x,y))
        elif type=="red":
            self.image = pygame.image.load('assets/pixel_laser_red.png').convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
        elif type =="blue":
            self.image = pygame.image.load('assets/pixel_laser_blue.png').convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
        elif type =="green":
            self.image = pygame.image.load('assets/pixel_laser_green.png').convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))

        self.mask = pygame.mask.from_surface(self.image)

    def destroy_laser(self):
        self.kill()

    def animate_laser(self):
        if self.type == "yellow":
            self.rect.y -= self.speed
            if self.rect.bottom <0:
                self.kill()
        else:
            self.rect.y += self.speed
            if self.rect.top > 650:
                self.kill()

    def update(self):
        self.animate_laser()
