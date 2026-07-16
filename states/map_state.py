import pygame
from states.base_state import GameState
from states.location import Location
from core.level import Level
from entities.enemy import Enemy
from ui.inventory_ui import InventoryUI

class MapState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.inventory_ui = InventoryUI(self.game.player.inventory, x=200, y=100)
        self.current_location = Location((20, 30, 20), (600, 300, 50, 50), (380, 50, 50, 50))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventory_ui.toggle()
        
            self.inventory_ui.handle_event(event)

    def update(self):
        self.game.player.update()
        next_state = self.current_location.update(self.game.player)

        if next_state == 'BATTLE':
            test_level = Level('Тестовая арена', [[Enemy()], [Enemy(), Enemy()]])
            self.game.change_state('BATTLE', level=test_level)
            
        elif next_state == 'NEXT_LOC':
            print("Телепортация в следующую комнату!")
            self.game.player.rect.x = 400
            self.game.player.rect.y = 500

    def draw(self, screen):
        self.current_location.draw(screen)
        self.game.player.draw(screen)
        self.inventory_ui.draw(screen)