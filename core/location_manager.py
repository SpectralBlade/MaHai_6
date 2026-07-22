import os
import json
import pygame
from core import asset_manager

class Portal:
    def __init__(self, data: dict):
        self.rect = pygame.Rect(data.get("x", 0), data.get("y", 0), data.get("width", 50), data.get("height", 50))
        self.type = data.get("type", "unknown")
        self.target_location_id = data.get("target_location_id")
        self.target_spawn_x = data.get("target_spawn_x", 0)
        self.target_spawn_y = data.get("target_spawn_y", 0)
        self.target_stage_id = data.get("target_stage_id")

class Location:
    def __init__(self, location_id: str, data: dict):
        self.location_id = location_id
        self.name = data.get("comment", "Unknown")
        self.map_size_x = data.get("map_size_x", 800)
        self.map_size_y = data.get("map_size_y", 600)
        
        bg_name = data.get("map_grid_background")
        if bg_name:
            img = asset_manager.get_image(bg_name)
            self.background = pygame.transform.scale(img, (self.map_size_x, self.map_size_y))
        else:
            self.background = pygame.Surface((self.map_size_x, self.map_size_y))
            self.background.fill((50, 100, 50))
            
        self.barriers = [pygame.Rect(b["x"], b["y"], b["width"], b["height"]) for b in data.get("barriers", [])]
        
        self.portals = []
        portals_data = data.get("interactibles", {}).get("portals", [])
        for p_data in portals_data:
            self.portals.append(Portal(p_data))

    def draw(self, screen, camera):
        screen.blit(self.background, (camera.camera.x, camera.camera.y))
        
        for b in self.barriers:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(b), 2)
            
        for p in self.portals:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply_rect(p.rect), 2)

_locations_db = {}

def init():
    global _locations_db
    path = os.path.join(asset_manager.ROOT_DIR, 'assets', 'data', 'world_parts.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            _locations_db = json.load(f)
        print(f"Загружено {len(_locations_db)} локаций.")
    except Exception as e:
        print(f"Ошибка загрузки world_parts.json: {e}")

def create_location(location_id: str) -> Location | None:
    if location_id not in _locations_db:
        print(f"Локация '{location_id}' не найдена!")
        return None
    return Location(location_id, _locations_db[location_id])