from curses import KEY_RIGHT
from Laser import Laser
import pygame

class MainCraft(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load('assets/pixel_ship_yellow.png').convert_alpha()
        self.rect = self.image.get_rect(center=(375, 550))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.previous_time = 0
        self.current_time = 0
        self.lasers = pygame.sprite.Group()
        self.laser_sound_effect = pygame.mixer.Sound('assets/audio/laser.wav')
        self.laser_sound_effect.set_volume(0.2)

    def shoot_laser(self):
        self.lasers.add(Laser("yellow", self.rect.x, self.rect.y+50))
        self.laser_sound_effect.play()
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.right+self.speed >= 750:
                self.rect.right = 750
            else:
                self.rect.x += self.speed
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            if self.rect.left -self.speed <= 0:
                self.rect.left = -5
            else:
                self.rect.left -= self.speed
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            if self.rect.top-self.speed <= 0:
                self.rect.top = 0
            else:
                self.rect.y -= self.speed
        if keys[pygame.K_s]or keys[pygame.K_DOWN]:
            if self.rect.bottom >= 650:
                self.rect.bottom = 650
            else:
                self.rect.y += self.speed
        if keys[pygame.K_SPACE] and (self.current_time - self.previous_time) >= 600:
            self.shoot_laser()
            self.previous_time = self.current_time


    def update(self, current_time):
        self.player_input()
        self.current_time= current_time
        self.lasers.update()


