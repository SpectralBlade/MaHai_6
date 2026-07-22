import pygame
import random
from states.base_state import GameState
from ui.elements import Button
from core import item_manager, asset_manager

from core.settings import *

class VictoryState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.SysFont('arial', 48, bold=True)
        self.font_text = pygame.font.SysFont('arial', 20)
        self.font_small = pygame.font.SysFont('arial', 16)
        
        self.btn_continue = Button(325, 520, 150, 40, "Карта", self.font_text)
        self.summary_data = {}

    def enter(self, **kwargs):
        level = kwargs.get('level')
        profile = self.game.profile
        
        self.summary_data = {'party': profile.party, 'drops': []}
        
        base_xp = 100 
        xp_gained = int(base_xp * level.xp_modifier)
        self.summary_data['xp'] = xp_gained
        
        self.summary_data['old_levels'] = {char.character_id: char.level for char in profile.party}
        for char in profile.party:
            char.gain_xp(xp_gained)
            
        rewards = level.rewards
        is_first_clear = level.level_id not in profile.cleared_levels
        
        if is_first_clear:
            profile.cleared_levels.add(level.level_id)
            fc_award = rewards.get('first_clear_award')
            if fc_award:
                item = item_manager.create_item(fc_award['item_id'])
                if item:
                    profile.inventory.add_item(item, fc_award['amount'])
                    self.summary_data['drops'].append({'item': item, 'amount': fc_award['amount'], 'is_first': True})
        
            main_pool = rewards.get('main_reward_pool', [])
            for drop_info in main_pool:
                if random.random() <= drop_info['weight']:
                    item = item_manager.create_item(drop_info['item_id'])
                    if item:
                        profile.inventory.add_item(item, drop_info['amount'])
                        self.summary_data['drops'].append({'item': item, 'amount': drop_info['amount'], 'is_first': False})

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_continue.handle_event(event):
                    self.game.change_state('MAP')

    def update(self):
        self.btn_continue.update(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill((25, 45, 35))
        
        title = self.font_title.render("ПОБЕДА!", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))
        
        screen.blit(self.font_text.render("Опыт команды:", True, (200, 200, 255)), (50, 110))
        for i, char in enumerate(self.summary_data['party']):
            char_y = 150 + (i * 80)
            
            img = pygame.transform.scale(asset_manager.get_image(char.image_filename), (60, 60))
            screen.blit(img, (50, char_y))
            
            lvl_up = ""
            color = (255, 255, 255)
            if char.level > self.summary_data['old_levels'][char.character_id]:
                lvl_up = " (УРОВЕНЬ ПОВЫШЕН!)"
                color = (100, 255, 100)
            
            text_name = self.font_text.render(f"{char.name} | Ур. {char.level}{lvl_up}", True, color)
            text_xp = self.font_small.render(f"+{self.summary_data['xp']} XP (До след: {char.xp_to_next_level - char.current_xp})", True, (150, 150, 150))
            
            screen.blit(text_name, (125, char_y + 5))
            screen.blit(text_xp, (125, char_y + 35))
            
        screen.blit(self.font_text.render("Полученные предметы:", True, (255, 200, 200)), (450, 110))
        for i, drop in enumerate(self.summary_data['drops']):
            drop_y = 150 + (i * 60)
            
            img = pygame.transform.scale(drop['item'].image, (40, 40))
            screen.blit(img, (450, drop_y))
            
            color = (255, 215, 0) if drop['is_first'] else (200, 200, 200)
            prefix = "[1st Clear] " if drop['is_first'] else ""
            
            text = self.font_text.render(f"{prefix}{drop['item'].name} x{drop['amount']}", True, color)
            screen.blit(text, (500, drop_y + 10))
            
        self.btn_continue.draw(screen)