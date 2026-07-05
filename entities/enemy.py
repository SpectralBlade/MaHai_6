import pygame
from core.settings import *
from components.character import Character
from core import asset_manager

class Enemy():
    def __init__(self):

        masha = asset_manager.get_image('MASHUSHA.png')

        self.mini_masha = pygame.transform.scale(masha, (80, 80))

        self.rect = pygame.Rect(0, 0, 40, 40)
        self.speed = 2
        self.hp = 100
        self.stats = Character(name = 'Приспешник Машуши', max_hp = 50, attack = 5)

    def update(self, player):
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed
        
    def draw(self, screen):
        screen.blit(self.mini_masha, self.rect)