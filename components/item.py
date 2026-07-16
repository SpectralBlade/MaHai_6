from __future__ import annotations
from core import asset_manager

class Item:
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int,
                 image_filename: str, buy_cost: int = 0, max_stack: int = 1):
        self.item_id = item_id
        self.name = name
        self.rarity = rarity
        self.sell_cost = sell_cost
        self.buy_cost = buy_cost
        self.max_stack = max_stack
        self.image = asset_manager.get_image(image_filename)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

class Equipment(Item):
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int, 
                 image_filename: str, stats_bonus: dict, enchantable: bool = False, buy_cost: int = 0):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, max_stack=1)
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
                 image_filename: str, effect_type: str, effect_value: int, buy_cost: int = 0):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, max_stack=99)
        self.effect_type = effect_type
        self.effect_value = effect_value

    def use(self, target_character) -> bool:
        if self.effect_type == 'heal':
            target_character.current_hp = min(target_character.current_hp + self.effect_value,
                                              target_character.max_hp)
            print(f"{target_character.name} восстановил {self.effect_value} ХП!")
            return True
        return False

class Material(Item):
    def __init__(self, item_id: str, name: str, rarity: str, sell_cost: int, image_filename: str, buy_cost: int = 0):
        super().__init__(item_id, name, rarity, sell_cost, image_filename, buy_cost, max_stack=99)

class QuestItem(Item):
    def __init__(self, item_id: str, name: str, image_filename: str):
        super().__init__(item_id, name, rarity="Quest", sell_cost=0, image_filename=image_filename, max_stack=1)
        self.can_be_dropped = False
        self.can_be_sold = False