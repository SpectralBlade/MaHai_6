from settings import *
from classes.player import *
from enemy import *
import pygame
from classes.level import Level

class BattleManager():
    def __init__(self, player: Player, level: Level):
        self.level = level
        self.enemies = self.level.get_current_enemies()

        self.font = pygame.font.SysFont('arial', 24)

        self.attack_button = pygame.Rect(160, 310, 80, 30)
        self.heal_button = pygame.Rect(160, 340, 80, 30)
                                
        self.player = player

        player.rect.x = 150
        player.rect.y = 400

        self.turn = 'PLAYER'

        self.selected_target = None

        self.show_menu = False

    def draw(self, screen):
        self.player.draw(screen)
        enemy_x = 600
        enemy_y = 200
        i = 0
        
        for enemy in self.enemies:
            enemy.rect.x = enemy_x
            enemy.rect.y = enemy_y + (i * 60)
            enemy.draw(screen)
            enemy_hp_text = self.font.render(f'HP врага: {enemy.stats.current_hp}', True, (255, 255, 255))
            screen.blit(enemy_hp_text, (600, 200 + (i * 60)))
            i += 1

        player_hp_text = self.font.render(f'Ваш HP: {self.player.stats.current_hp}', True, (255, 255, 255))
        screen.blit(player_hp_text, (150, 450))
        
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
                    self.turn = 'ENEMY'
                    self.show_menu = False
            elif self.heal_button.collidepoint(mouse_pos):
                self.player.stats.current_hp += 30
                if self.player.stats.current_hp > self.player.stats.max_hp:
                    self.player.stats.current_hp = self.player.stats.max_hp
                self.show_menu = False
                self.turn = 'ENEMY'

        else:
            for enemy in self.enemies:
                if enemy.rect.collidepoint(mouse_pos):
                    self.selected_target = enemy
                elif self.player.rect.collidepoint(mouse_pos):
                    self.show_menu = True
    
    def update(self):

        if self.enemies[0].stats.current_hp <= 0:
            return 'MAP'
        
        if self.turn == 'ENEMY':
            self.player.stats.take_damage(20)
            self.turn = 'PLAYER'

        if self.player.stats.current_hp <= 0:
            print('Волосня поглотила вас')
            return 'GAME_OVER'
            
        return 'BATTLE'