import pygame
import os

_images = {}
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_image(filename: str) -> pygame.Surface:
    if filename not in _images:
        path = os.path.join(ROOT_DIR, 'assets', 'images', filename)
        
        try:
            image = pygame.image.load(path).convert_alpha()
            _images[filename] = image
        except FileNotFoundError:
            print(f"[ОШИБКА] Не удалось найти изображение: {path}")
            
            fallback_surface = pygame.Surface((80, 80))
            fallback_surface.fill((255, 0, 255))
            _images[filename] = fallback_surface
            
    return _images[filename]