from settings import *
from classes.player import *
from enemy import *
import pygame

class BattleManager():
    def __init__(self, player, enemy):

        self.font = pygame.font.SysFont('arial', 24)

        self.attack_button = pygame.Rect(160, 310, 80, 30)
        self.heal_button = pygame.Rect(160, 340, 80, 30)
                                
        self.player = player
        self.enemy = enemy

        player.rect.x = 150
        player.rect.y = 400

        enemy.rect.x = 600
        enemy.rect.y = 400

        self.turn = 'PLAYER'

        self.selected_target = None

        self.show_menu = False

    def draw(self, screen):
        self.player.draw(screen)
        self.enemy.draw(screen)

        if self.show_menu:
            pygame.draw.rect(screen, (30, 30, 30), (150, 300, 120, 80))
            attack_text = self.font.render('Атака', True, (255, 255, 255))
            heal_text = self.font.render('Лечение', True, (255, 255, 255))
            screen.blit(attack_text, (160, 310))
            screen.blit(heal_text, (160, 340))


    def handle_click(self, mouse_pos):
        if self.show_menu == True:
            if self.attack_button.collidepoint(mouse_pos):
                if self.selected_target != None:
                    self.selected_target.stats.take_damage(self.player.stats.attack)
                    self.show_menu = False
        else:
            if self.enemy.rect.collidepoint(mouse_pos):
                self.selected_target = self.enemy
            elif self.player.rect.collidepoint(mouse_pos):
                self.show_menu = True