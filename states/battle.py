from core.settings import *
from entities.player import *
from entities.enemy import *
import pygame
from core.level import Level

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
        
        for i, enemy in enumerate(self.enemies):
            enemy.rect.x = 600
            enemy.rect.y = 200 + (i * 60)
            enemy.draw(screen)
            
            hp_text = self.font.render(f'HP: {enemy.stats.current_hp}', True, (255, 255, 255))
            screen.blit(hp_text, (650, 200 + (i * 60)))

            if self.selected_target == enemy:
                pygame.draw.rect(screen, (255, 0, 0), enemy.rect, 2)
        
        player_hp_text = self.font.render(f'Ваш HP: {self.player.stats.current_hp}', True, (255, 255, 255))
        screen.blit(player_hp_text, (150, 450))
        
        if self.show_menu:
            pygame.draw.rect(screen, (30, 30, 30), (150, 300, 120, 80))
            attack_text = self.font.render('Атака', True, (255, 255, 255))
            heal_text = self.font.render('Лечение', True, (255, 255, 255))
            screen.blit(attack_text, (160, 310))
            screen.blit(heal_text, (160, 340))


    def handle_click(self, mouse_pos):
        if self.turn != 'PLAYER':
            return
            
        for enemy in self.enemies:
            if enemy.rect.collidepoint(mouse_pos):
                self.selected_target = enemy
                print(f"Выбрана цель: {enemy.stats.name}") 

        if self.show_menu:
            if self.attack_button.collidepoint(mouse_pos):
                
                if self.selected_target not in self.enemies:
                    if self.enemies:
                        self.selected_target = self.enemies[0]
                
                if self.selected_target:
                    self.selected_target.stats.take_damage(self.player.stats.attack)
                    self.turn = 'ENEMY'
                    self.show_menu = False
                    
            elif self.heal_button.collidepoint(mouse_pos):
                self.player.stats.current_hp = min(self.player.stats.current_hp + 30, self.player.stats.max_hp)
                self.turn = 'ENEMY'
                self.show_menu = False
                
        else:
            if self.player.rect.collidepoint(mouse_pos):
                self.show_menu = True

    def update(self):
        self.enemies = [e for e in self.enemies if e.stats.current_hp > 0]
        
        if len(self.enemies) == 0:
            self.level.next_wave()
            
            if self.level.is_completed():
                return 'MAP'
            else:
                self.enemies = self.level.get_current_enemies()
                self.selected_target = None
                self.show_menu = True
                return 'BATTLE'

        # 3. Логика хода врагов
        if self.turn == 'ENEMY':
            for enemy in self.enemies:
                self.player.stats.take_damage(enemy.stats.attack)
            self.turn = 'PLAYER'
            self.show_menu = True

        # 4. Проверка смерти игрока
        if self.player.stats.current_hp <= 0:
            print('Волосня поглотила вас')
            return 'GAME_OVER'
            
        return 'BATTLE'
