import pygame
import random
from ui.elements import Panel, Button
from core import asset_manager

class BattleManager:
    def __init__(self, profile, level):
        self.profile = profile
        self.party = [char for char in profile.party if char.current_hp > 0]
        
        self.level = level
        self.enemies = self.level.get_current_enemies()
        
        self.turn = 'PLAYER'
        self.current_actor_index = 0 
        self.selected_target = None
        self.show_menu = True
        
        self.font = pygame.font.SysFont('arial', 24)
        
        self.menu_panel = Panel(200, 450, 140, 90)
        self.btn_attack = Button(210, 460, 120, 30, 'Атака', self.font)
        self.btn_heal = Button(210, 500, 120, 30, 'Пропуск', self.font) 

        self.party_images = {}
        for char in self.party:
            img = asset_manager.get_image(char.image_filename)
            self.party_images[char.character_id] = pygame.transform.scale(img, (60, 60))

    def handle_event(self, event):
        if self.turn != 'PLAYER' or not self.party:
            return

        active_character = self.party[self.current_actor_index]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            for enemy in self.enemies:
                if enemy.rect.collidepoint(mouse_pos):
                    self.selected_target = enemy
                    print(f"Выбрана цель: {enemy.stats.name}")

        if self.show_menu:
            if self.btn_attack.handle_event(event):
                if not self.selected_target and self.enemies:
                    self.selected_target = self.enemies[0]
                    
                if self.selected_target:
                    print(f"{active_character.name} наносит {active_character.total_attack} урона!")
                    self.selected_target.stats.take_damage(active_character.total_attack)
                    self._next_turn()
                    
            elif self.btn_heal.handle_event(event):
                print(f"{active_character.name} пропускает ход.")
                self._next_turn()

    def _next_turn(self):
        self.selected_target = None
        self.current_actor_index += 1
        
        if self.current_actor_index >= len(self.party):
            self.turn = 'ENEMY'
            self.show_menu = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.show_menu and self.turn == 'PLAYER':
            self.btn_attack.update(mouse_pos)
            self.btn_heal.update(mouse_pos)

        self.enemies = [e for e in self.enemies if e.stats.current_hp > 0]
        
        if len(self.enemies) == 0:
            self.level.next_wave()
            
            if self.level.is_completed():
                print("Бой побежден!")
                for char in self.party:
                    char.current_hp = char.total_max_hp
                return 'VICTORY'
            else:
                print(f"Начинается фаза {self.level.current_wave_index + 1}!")
                self.enemies = self.level.get_current_enemies()
                
                self.turn = 'PLAYER'
                self.current_actor_index = 0
                self.selected_target = None
                self.show_menu = True
                return 'BATTLE'

        self.party = [char for char in self.party if char.current_hp > 0]
        if not self.party:
            print("Команда разбита...")
            return 'GAME_OVER'

        if self.turn == 'ENEMY':
            for enemy in self.enemies:
                target = random.choice(self.party)
                print(f"{enemy.stats.name} атакует {target.name} на {enemy.stats.attack} урона!")
                target.take_damage(enemy.stats.attack)
                
            self.turn = 'PLAYER'
            self.current_actor_index = 0
            self.show_menu = True
            
        return 'BATTLE'

    def draw(self, screen):
        for i, char in enumerate(self.party):
            char_x = 100
            char_y = 150 + (i * 100)
            
            screen.blit(self.party_images[char.character_id], (char_x, char_y))
            
            if self.turn == 'PLAYER' and i == self.current_actor_index:
                pygame.draw.rect(screen, (0, 255, 0), (char_x, char_y, 60, 60), 3)
                
            hp_text = self.font.render(f'{char.name} HP: {char.current_hp}/{char.total_max_hp}', True, (100, 255, 100))
            screen.blit(hp_text, (char_x - 20, char_y + 70))

        for i, enemy in enumerate(self.enemies):
            enemy.rect.x = 600
            enemy.rect.y = 150 + (i * 100)
            enemy.draw(screen)
            
            if self.selected_target == enemy:
                pygame.draw.rect(screen, (255, 0, 0), enemy.rect, 3)
                
            hp_text = self.font.render(f'HP: {enemy.stats.current_hp}/{enemy.stats.max_hp}', True, (255, 100, 100))
            screen.blit(hp_text, (enemy.rect.x, enemy.rect.y + 85))

        if self.turn == 'PLAYER' and self.show_menu:
            self.menu_panel.draw(screen)
            self.btn_attack.draw(screen)
            self.btn_heal.draw(screen)