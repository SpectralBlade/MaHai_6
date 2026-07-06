import pygame

class Panel:
    def __init__(self, x, y, width, height, bg_color=(30, 30, 30), border_color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)


class Button:
    def __init__(self, x, y, width, height, text, font, bg_color=(50, 50, 50), hover_color=(80, 80, 80),
                 text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered else self.bg_color

        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)