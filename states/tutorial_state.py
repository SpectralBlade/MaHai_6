import pygame
from states.base_state import GameState
from core.settings import *
from core import asset_manager

class TutorialState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont('arial', 42, bold=True)
        self.name_font = pygame.font.SysFont('arial', 24)

        img1 = asset_manager.get_image('MERMUSH_V_PRAIME.png')
        self.hero1_image = pygame.transform.scale(img1, (120, 120))
        self.hero1_rect = self.hero1_image.get_rect(center=(WIDTH // 3, HEIGHT // 2))

        img2 = asset_manager.get_image('MASHUSHA.png')
        self.hero2_image = pygame.transform.scale(img2, (120, 120))
        self.hero2_rect = self.hero2_image.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if self.hero1_rect.collidepoint(mouse_pos):
                    self._select_hero("spectrum")
                elif self.hero2_rect.collidepoint(mouse_pos):
                    self._select_hero("masha")

    def _select_hero(self, character_id: str):
        self.game.profile.choose_starter(character_id)
        self.game.player.update_avatar()
        self.game.change_state('MAP')

    def draw(self, screen):
        screen.fill((30, 30, 45))
        
        title = self.title_font.render("Выберите основного персонажа", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        screen.blit(self.hero1_image, self.hero1_rect)
        name1 = self.name_font.render("Spectrum", True, (200, 200, 200))
        screen.blit(name1, name1.get_rect(center=(self.hero1_rect.centerx, self.hero1_rect.bottom + 20)))

        screen.blit(self.hero2_image, self.hero2_rect)
        name2 = self.name_font.render("Машуша", True, (200, 200, 200))
        screen.blit(name2, name2.get_rect(center=(self.hero2_rect.centerx, self.hero2_rect.bottom + 20)))