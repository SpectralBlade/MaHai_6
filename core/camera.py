import pygame
from core.settings import WIDTH, HEIGHT

class Camera:
    def __init__(self, map_width: int, map_height: int):
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect: pygame.Rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - WIDTH), x)
        y = max(-(self.map_height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)