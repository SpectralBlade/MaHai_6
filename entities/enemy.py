import pygame
from components.character import Character
from core import asset_manager

class Enemy:
    def __init__(self):
        self.stats = Character(name='Приспешник Машуши', max_hp=50, attack=5)

        masha = asset_manager.get_image('MASHUSHA.png')
        self.image = pygame.transform.scale(masha, (80, 80))

        self.rect = self.image.get_rect() 

    def draw(self, screen):
        screen.blit(self.image, self.rect)