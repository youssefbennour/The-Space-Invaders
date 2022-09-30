import pygame
from random import choice, randint
from Laser import Laser

class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y,pace=randint(1,7), speed=200):
        super().__init__()
        self.invader_type = choice(['blue', 'green', 'red'])
        if self.invader_type == 'red':
            self.image = pygame.image.load('assets/pixel_ship_red_small.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft= (x,y))
        elif self.invader_type == 'blue':
            self.image = pygame.image.load('assets/pixel_ship_blue_small.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft= (x,y))
        elif self.invader_type == 'green':
            self.image = pygame.image.load('assets/pixel_ship_green_small.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft= (x,y))


        self.mask = pygame.mask.from_surface(self.image)
        self.lasers = pygame.sprite.Group()
        self.direction = -1
        self.pace_size = pace
        self.pace_count = 0
        self.pace_time = 0
        self.speed = speed
        self.turn_after = randint(1,4)
    def destroy_laser(self):
        self.kill();
    def animate_invader(self):
        if self.rect.y >= 650:
            self.kill()
        self.rect.y += 1
        current_time = pygame.time.get_ticks()
        if current_time >= (self.pace_time + self.speed):
            self.pace_time = current_time
            self.pace_count += 1
            self.rect.x += self.pace_size*self.direction

            if self.pace_count%self.turn_after == 0 or self.rect.left<0 or self.rect.right>750:
                self.direction *= -1
                self.pace_count = 0
                self.pace_size = randint(1,7)
                self.turn_after = randint(1,4)

    def update(self):
        self.animate_invader()
