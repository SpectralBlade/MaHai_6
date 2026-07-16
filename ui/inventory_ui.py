import pygame
from ui.elements import Panel
from components.inventory import Inventory

class InventoryUI:
    def __init__(self, inventory: Inventory, x: int, y: int):
        self.inventory = inventory
        self.x = x
        self.y = y
        
        self.cols = 5
        self.rows = 4 
        self.slot_size = 50
        self.padding = 10
        
        width = self.cols * (self.slot_size + self.padding) + self.padding
        height = self.rows * (self.slot_size + self.padding) + self.padding
        
        self.panel = Panel(x, y, width, height, bg_color=(40, 40, 40), border_color=(150, 150, 150))
        self.font = pygame.font.SysFont('arial', 16)
        
        self.is_open = False

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event: pygame.event.Event):
        if not self.is_open:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.panel.rect.collidepoint(mouse_pos):
                print("Клик по инвентарю!")
                return True
        return False

    def draw(self, screen: pygame.Surface):
        if not self.is_open:
            return
            
        self.panel.draw(screen)

        for i, slot in enumerate(self.inventory.slots):
            col = i % self.cols
            row = i // self.cols
            
            slot_x = self.x + self.padding + (self.slot_size + self.padding) * col
            slot_y = self.y + self.padding + (self.slot_size + self.padding) * row
            
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            pygame.draw.rect(screen, (60, 60, 60), slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), slot_rect, 1)

            if not slot.is_empty:
                item_image = pygame.transform.scale(slot.item.image, (self.slot_size, self.slot_size))
                screen.blit(item_image, slot_rect)
                
                if slot.quantity > 1:
                    text_surface = self.font.render(str(slot.quantity), True, (255, 255, 255))
                    
                    text_rect = text_surface.get_rect(bottomright=(slot_rect.right - 2, slot_rect.bottom - 2))
                    
                    screen.blit(text_surface, text_rect)
