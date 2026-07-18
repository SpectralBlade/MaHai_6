import pygame
from ui.elements import Panel, Button
from components.item import Equipment, Consumable

class InventoryUI:
    def __init__(self, profile, x: int, y: int):
        self.profile = profile
        self.inventory = profile.inventory
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
        self.title_font = pygame.font.SysFont('arial', 20, bold=True)
        
        self.is_open = False
        self.selected_item = None

        desc_x = self.x + self.panel.rect.width + 10
        self.btn_action = Button(desc_x + 35, self.y + 150, 150, 30, "Действие", self.font)

    def toggle(self):
        self.is_open = not self.is_open
        if not self.is_open:
            self.selected_item = None 

    def handle_event(self, event: pygame.event.Event):
        if not self.is_open:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if self.selected_item:
                self.btn_action.update(mouse_pos)
                if self.btn_action.handle_event(event):
                    self._perform_action()
                    return True

            for i, slot in enumerate(self.inventory.slots):
                col = i % self.cols
                row = i // self.cols
                slot_x = self.x + self.padding + (self.slot_size + self.padding) * col
                slot_y = self.y + self.padding + (self.slot_size + self.padding) * row
                slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
                
                if slot_rect.collidepoint(mouse_pos):
                    if not slot.is_empty:
                        self.selected_item = slot.item
                    else:
                        self.selected_item = None
                    return True
        return False

    def _perform_action(self):
        if not self.profile.party:
            print("В команде нет персонажей!")
            return

        active_character = self.profile.party[0]

        if isinstance(self.selected_item, Equipment):
            self.inventory.remove_item(self.selected_item.item_id, 1)
            
            old_item = active_character.equip_item(self.selected_item)
            
            if old_item:
                self.inventory.add_item(old_item, 1)
                
            print(f"Текущая атака {active_character.name}: {active_character.total_attack}")
            self.selected_item = None
            
        elif isinstance(self.selected_item, Consumable):
            success = self.selected_item.use(active_character)
            if success:
                self.inventory.remove_item(self.selected_item.item_id, 1)
                
                remaining = sum(s.quantity for s in self.inventory.slots 
                              if not s.is_empty and s.item.item_id == self.selected_item.item_id)
                if remaining <= 0:
                    self.selected_item = None

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
            
            bg_color = (100, 100, 50) if self.selected_item == slot.item else (60, 60, 60)
            pygame.draw.rect(screen, bg_color, slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), slot_rect, 1)

            if not slot.is_empty:
                item_image = pygame.transform.scale(slot.item.image, (self.slot_size, self.slot_size))
                screen.blit(item_image, slot_rect)
                
                if slot.quantity > 1:
                    text_surface = self.font.render(str(slot.quantity), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(bottomright=(slot_rect.right - 2, slot_rect.bottom - 2))
                    screen.blit(text_surface, text_rect)
                    
        if self.selected_item:
            desc_width = 220
            desc_x = self.x + self.panel.rect.width + 10
            desc_y = self.y
            
            pygame.draw.rect(screen, (30, 30, 30), (desc_x, desc_y, desc_width, self.panel.rect.height))
            pygame.draw.rect(screen, (200, 200, 200), (desc_x, desc_y, desc_width, self.panel.rect.height), 2)
            
            name_text = self.title_font.render(self.selected_item.name, True, (255, 215, 0))
            screen.blit(name_text, (desc_x + 10, desc_y + 10))
            
            type_text = self.font.render(f"Тип: {self.selected_item.__class__.__name__}", True, (150, 150, 255))
            screen.blit(type_text, (desc_x + 10, desc_y + 40))
            
            lore_text = self.font.render(self.selected_item.lore, True, (150, 150, 150))
            screen.blit(lore_text, (desc_x + 10, desc_y + 80))
      
            mouse_pos = pygame.mouse.get_pos()
            
            if isinstance(self.selected_item, Equipment):
                self.btn_action.text = "Экипировать"
                self.btn_action.update(mouse_pos)
                self.btn_action.draw(screen)
                
            elif isinstance(self.selected_item, Consumable):
                self.btn_action.text = "Использовать"
                self.btn_action.update(mouse_pos)
                self.btn_action.draw(screen)