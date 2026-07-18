import pygame
from core.settings import *
from core import asset_manager

class Player:
    def __init__(self, profile, x=400, y=300):
        self.profile = profile
        
        mermush = asset_manager.get_image('MERMUSH_V_PRAIME.png')
        self.image = pygame.transform.scale(mermush, (80, 80))
        self.rect = pygame.Rect(x, y, 40, 40)
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

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT 
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)