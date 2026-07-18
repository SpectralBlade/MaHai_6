import pygame
from core.settings import *
from entities.player import Player
from core import item_manager
from core.profile import Profile

from states.map_state import MapState
from states.battle_state import BattleState
from states.game_over_state import GameOverState

class Game:
    def __init__(self):
        pygame.init()
        item_manager.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mermush RPG")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.profile = Profile()
        self.player = Player(self.profile)

        self.states = {
            'MAP': MapState(self),
            'BATTLE': BattleState(self),
            'GAME_OVER': GameOverState(self)
        }
        
        self.current_state = self.states['MAP']
        self.current_state.enter()

    def change_state(self, next_state_name: str, **kwargs):
        if next_state_name in self.states:
            self.current_state = self.states[next_state_name]
            self.current_state.enter(**kwargs)
        else:
            print(f"[ОШИБКА] Состояние {next_state_name} не существует в реестре игры!")

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_state.handle_events(events)
            
            self.current_state.update()
            
            self.screen.fill(BG_COLOR)
            self.current_state.draw(self.screen)
            
            pygame.display.flip()
            
        pygame.quit()