import pygame
from core.settings import *
from core import asset_manager

class Player:
    def __init__(self, profile, x=400, y=300):
        self.profile = profile 
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
        self.image = None

    def update_avatar(self):
        if not self.profile.party:
            return
        leader = self.profile.party[0]
        img = asset_manager.get_image(leader.image_filename)
        self.image = pygame.transform.scale(img, (80, 80))
        
    def update(self, barriers: list[pygame.Rect]):
        keys = pygame.key.get_pressed()
        
        dx = 0
        dy = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy = self.speed

        if dx != 0:
            self.rect.x += dx
            if self.rect.collidelist(barriers) != -1:
                self.rect.x -= dx

        if dy != 0:
            self.rect.y += dy
            if self.rect.collidelist(barriers) != -1:
                self.rect.y -= dy

    def draw(self, screen, camera=None):
        if self.image:
            if camera:
                screen.blit(self.image, camera.apply(self))
            else:
                screen.blit(self.image, self.rect)