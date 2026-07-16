import pygame
from core.settings import *
from components.character import Character
from core import asset_manager, item_manager
from components.inventory import Inventory

from components.item import Consumable

class Player():


    def __init__(self):
        
        self.inventory = Inventory(capacity=20) 
        
        mermush = asset_manager.get_image('MERMUSH_V_PRAIME.png')

        potion = item_manager.create_item('health_potion_01')
        if potion:
            self.inventory.add_item(potion, amount=5)
            
        sword = item_manager.create_item('rusty_sword')
        if sword:
            self.inventory.add_item(sword, amount=1)

        self.mini_mermush = pygame.transform.scale(mermush, (80, 80))

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
        screen.blit(self.mini_mermush, self.rect)