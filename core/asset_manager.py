import pygame
import os

_images = {}

def get_image(filename: str) -> pygame.Surface:
    """
    Загружает изображение по имени файла или возвращает из кэша, если оно уже загружено.
    """
    if filename not in _images:
        path = os.path.join('assets', 'images', filename)
        
        try:
            image = pygame.image.load(path).convert_alpha()
            _images[filename] = image
        except FileNotFoundError:
            print(f"[ОШИБКА] Не удалось найти изображение: {path}")
            
            fallback_surface = pygame.Surface((80, 80))
            fallback_surface.fill((255, 0, 255))
            _images[filename] = fallback_surface
            
    return _images[filename]