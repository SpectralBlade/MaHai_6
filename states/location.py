import pygame
from core.settings import *

class Location:
    def __init__(self, bg_color, battle_gate_rect, next_gate_rect, level_data=None):

        self.bg_color = bg_color
        
        self.battle_gate = pygame.Rect(battle_gate_rect)
        self.next_gate = pygame.Rect(next_gate_rect)
        
        self.interactables = []
        
        self.level_data = level_data

    def draw(self, screen):
        screen.fill(self.bg_color)
        pygame.draw.rect(screen, (255, 0, 0), self.battle_gate)
        pygame.draw.rect(screen, (255, 255, 0), self.next_gate)
        
    def update(self, player):
        if player.rect.colliderect(self.battle_gate):
            return "BATTLE"
        elif player.rect.colliderect(self.next_gate):
            return "NEXT_LOC"
        return "MAP"