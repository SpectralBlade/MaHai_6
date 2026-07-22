import pygame
from states.base_state import GameState
from core import location_manager, level_manager
from core.camera import Camera
from ui.inventory_ui import InventoryUI

class MapState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.current_location = location_manager.create_location("1-1_after_tutorial_dorm")
        
        self.camera = Camera(self.current_location.map_size_x, self.current_location.map_size_y)
        
        self.inventory_ui = InventoryUI(self.game.profile, x=150, y=100)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.inventory_ui.toggle()
            self.inventory_ui.handle_event(event)

    def update(self):
        self.game.player.update(self.current_location.barriers)
        
        self.camera.update(self.game.player)
        
        for portal in self.current_location.portals:
            if self.game.player.rect.colliderect(portal.rect):
                self._handle_portal(portal)

    def _handle_portal(self, portal):
        if portal.type == "map_transition":
            print(f"Телепортация в: {portal.target_location_id}")
            new_loc = location_manager.create_location(portal.target_location_id)
            
            if new_loc:
                self.current_location = new_loc
                self.camera = Camera(new_loc.map_size_x, new_loc.map_size_y)
                self.game.player.rect.x = portal.target_spawn_x
                self.game.player.rect.y = portal.target_spawn_y
            else:
                self.game.player.rect.y -= 20 
                
        elif portal.type == "battle_trigger":
            print(f"Бой начинается! Уровень: {portal.target_stage_id}")
            self.game.player.rect.y -= 60 
            
            actual_level = level_manager.create_level(portal.target_stage_id)
            if actual_level:
                self.game.change_state('BATTLE', level=actual_level)
            else:
                print("[ОШИБКА] Не удалось загрузить уровень боя.")

    def draw(self, screen):
        self.current_location.draw(screen, self.camera)
        self.game.player.draw(screen, self.camera)
        self.inventory_ui.draw(screen)