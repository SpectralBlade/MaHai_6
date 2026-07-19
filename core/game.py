import pygame
from core.settings import *
from entities.player import Player
from core import item_manager
from core.profile import Profile

from core import item_manager
from core import character_manager
from core import enemy_manager
from core import level_manager

from states.map_state import MapState
from states.battle_state import BattleState
from states.game_over_state import GameOverState
from states.tutorial_state import TutorialState

class Game:
    def __init__(self):
        pygame.init()

        item_manager.init()
        character_manager.init()
        enemy_manager.init()
        level_manager.init()   
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MaHai 6")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.profile = Profile()
        self.player = Player(self.profile)

        self.states = {
            'MAP': MapState(self),
            'BATTLE': BattleState(self),
            'GAME_OVER': GameOverState(self),
            'TUTORIAL_SCREEN': TutorialState(self)
        }
        
        self.current_state = self.states['TUTORIAL_SCREEN']
        self.current_state.enter()

    def change_state(self, next_state_name: str, **kwargs):
        if next_state_name in self.states:
            self.current_state = self.states[next_state_name]
            self.current_state.enter(**kwargs)
        else:
            print(f"Состояние {next_state_name} не существует в реестре игры!")

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