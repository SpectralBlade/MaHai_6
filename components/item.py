from __future__ import annotations
from core import asset_manager
from components.effects import Effect

class Item:
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int,
                 image_filename: str, buy_cost: int = 0, lore: str = "", max_stack: int = 1):
        self.item_id = item_id
        self.name = name
        self.rarity = rarity
        self.sell_cost = sell_cost
        self.buy_cost = buy_cost
        self.lore = lore
        self.max_stack = max_stack
        self.image = asset_manager.get_image(image_filename)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

class Equipment(Item):
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int, 
                 image_filename: str, stats_bonus: dict, equip_type: str, enchantable: bool = False, buy_cost: int = 0, lore: str = ""):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, lore, max_stack=1)
        self.equip_type = equip_type
        self.stats_bonus = stats_bonus
        self.enchantable = enchantable
        self.applied_enchantments = []

    def apply_enchantment(self, enchantment_scroll: Item) -> bool:
        if not self.enchantable:
            print(f"{self.name} нельзя зачаровать!")
            return False
        self.applied_enchantments.append(enchantment_scroll)
        print(f"На {self.name} успешно наложено зачарование!")
        return True

class Consumable(Item):
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int,
                 image_filename: str, effects: list[dict], buy_cost: int = 0, lore: str = ""):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, lore, max_stack=99)
        
        self.effects = [Effect(**eff_data) for eff_data in effects]

    def use(self, target_character) -> bool:
        if not self.effects:
            print(f"{self.name} не имеет эффектов!")
            return False
            
        for effect in self.effects:
            effect.apply(user=target_character, target=target_character)
            
        return True

class Material(Item):
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int, 
                 image_filename: str, lore: str = "", buy_cost: int = 0):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, lore, max_stack=99)

class QuestItem(Item):
    def __init__(self, item_id: str, name: str, rarity: str, image_filename: str, lore: str = ""):
        super().__init__(item_id, name, rarity, sell_cost=0, image_filename=image_filename, lore=lore, max_stack=1)
        self.can_be_dropped = False
        self.can_be_sold = False