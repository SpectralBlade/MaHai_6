import pygame
from settings import *
from classes.character import Character

class Enemy():
    def __init__(self):
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
        pygame.draw.rect(screen, (0, 255, 0), self.rect)