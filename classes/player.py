import pygame
from settings import *
from classes.character import Character

class Player():


    def __init__(self):

        self.rect = pygame.Rect(400, 300, 40, 40)
        self.stats = Character(name = 'Spectrum', max_hp = 100, max_mana = 50, attack = 15, resists = [])
        self.speed = 5
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT 
        

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)