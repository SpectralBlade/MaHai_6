import pygame
from ui.elements import Panel, Button

class BattleManager():
    def __init__(self, player, level):
        self.level = level
        self.enemies = self.level.get_current_enemies()
        self.player = player

        self.player.rect.x = 150
        self.player.rect.y = 400

        self.turn = 'PLAYER'
        self.selected_target = None
        self.show_menu = True

        self.font = pygame.font.SysFont('arial', 24)

        self.menu_panel = Panel(140, 300, 140, 90)
        self.btn_attack = Button(150, 310, 120, 30, 'Атака', self.font)
        self.btn_heal = Button(150, 350, 120, 30, 'Лечение', self.font)

    def handle_event(self, event):
        if self.turn != 'PLAYER':
            return

        if self.show_menu:
            if self.btn_attack.handle_event(event):
                if self.selected_target not in self.enemies:
                    if self.enemies:
                        self.selected_target = self.enemies[0]

                if self.selected_target:
                    self.selected_target.stats.take_damage(self.player.stats.attack)
                    self.turn = 'ENEMY'
                    self.show_menu = False

            elif self.btn_heal.handle_event(event):
                self.player.stats.current_hp = min(self.player.stats.current_hp + 30, self.player.stats.max_hp)
                self.turn = 'ENEMY'
                self.show_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            for enemy in self.enemies:
                if enemy.rect.collidepoint(mouse_pos):
                    self.selected_target = enemy
                    print(f"Выбрана цель: {enemy.stats.name}")

            if not self.show_menu and self.player.rect.collidepoint(mouse_pos):
                self.show_menu = True

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.show_menu:
            self.btn_attack.update(mouse_pos)
            self.btn_heal.update(mouse_pos)

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

        if self.turn == 'ENEMY':
            for enemy in self.enemies:
                self.player.stats.take_damage(enemy.stats.attack)
            self.turn = 'PLAYER'
            self.show_menu = True

        if self.player.stats.current_hp <= 0:
            return 'GAME_OVER'

        return 'BATTLE'

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
            self.menu_panel.draw(screen)
            self.btn_attack.draw(screen)
            self.btn_heal.draw(screen)
