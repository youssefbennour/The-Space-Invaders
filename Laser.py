import pygame
class Laser(pygame.sprite.Sprite):
    def __init__(self, type, x,y):
        super().__init__()
        self.type = type
        if type == "yellow":
            self.image = pygame.image.load('assets/pixel_laser_yellow.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft=(x,y))
        elif type=="red":
            self.image = pygame.image.load('assets/pixel_laser_red.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=(x,y))
        elif type =="blue":
            self.image = pygame.image.load('assets/pixel_laser_blue.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=(x,y))
        elif type =="green":
            self.image = pygame.image.load('assets/pixel_laser_green.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=(x,y))


    def destroy_laser(self):
        self.kill()

    def animate_laser(self):
        if self.type == "yellow":
            self.rect.y -= 6
            if self.rect.bottom <0:
                self.kill()
        else:
            self.rect.y += 6
            if self.rect.top > 650:
                self.kill()

    def update(self):
        self.animate_laser()