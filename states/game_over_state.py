import pygame
from states.base_state import GameState

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('arial', 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.player.stats.current_hp = self.game.player.stats.max_hp
                    self.game.change_state('MAP')

    def draw(self, screen):
        screen.fill((100, 0, 0)) 
        game_over_text = self.font.render('Волосня поглотила вас...', True, (255, 255, 255))
        press_space = self.font.render('Нажмите ПРОБЕЛ, чтобы продолжить', True, (255, 255, 255))
        screen.blit(press_space, (200, 200))
        screen.blit(game_over_text, (200, 300))