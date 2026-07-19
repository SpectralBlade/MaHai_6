import pygame
from components.character import Character
from core import asset_manager

class Enemy:
    def __init__(self, enemy_id: str, name: str, max_hp: int, attack: int, image_filename: str):
        self.enemy_id = enemy_id
        self.stats = Character(name=name, max_hp=max_hp, attack=attack)

        img = asset_manager.get_image(image_filename)
        self.image = pygame.transform.scale(img, (80, 80))
        self.rect = self.image.get_rect() 

    def draw(self, screen):
        screen.blit(self.image, self.rect)