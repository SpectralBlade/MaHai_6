from components.character import Character
from components.item import Equipment

class PlayableCharacter(Character):
    def __init__(self, character_id: str, name: str, max_hp: int, attack: int, max_mana: int = 0):
        super().__init__(name, max_hp, attack, resists=[], max_mana=max_mana)
        
        self.character_id = character_id
        
        self.level = 1
        self.current_xp = 0
        self.xp_to_next_level = 100
        
        self.equipment: dict[str, Equipment | None] = {
            "helmet": None,
            "chestplate": None,
            "pants": None,
            "boots": None, 
            "accessory_1": None,
            "accessory_2": None,
            "weapon": None,
        }

    @property
    def total_attack(self) -> int:
        equipment_bonus = 0
        for item in self.equipment.values():
            if item and hasattr(item, 'stats_bonus'):
                equipment_bonus += item.stats_bonus.get('attack', 0)
        return self.attack + equipment_bonus

    @property
    def total_max_hp(self) -> int:
        equipment_bonus = 0
        for item in self.equipment.values():
            if item and hasattr(item, 'stats_bonus'):
                equipment_bonus += item.stats_bonus.get('max_hp', 0)
        return self.max_hp + equipment_bonus

    def gain_xp(self, amount: int):
        self.current_xp += amount
        print(f"{self.name} получает {amount} XP!")
        
        while self.current_xp >= self.xp_to_next_level:
            self.current_xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.attack += 2
        self.current_hp = self.total_max_hp 
        self.xp_to_next_level = int(self.xp_to_next_level * 1.2)
        print(f"{self.name} достиг {self.level} уровня!")

    def equip_item(self, item: Equipment, specific_slot: str = None) -> Equipment | None:
        target_slot = specific_slot or item.equip_type
        
        if target_slot == "accessory":
            if self.equipment.get("accessory_1") is None:
                target_slot = "accessory_1"
            else:
                target_slot = "accessory_2"

        if target_slot not in self.equipment:
            print(f"У персонажа {self.name} нет слота '{target_slot}'!")
            return item

        old_item = self.equipment[target_slot]
        
        self.equipment[target_slot] = item
        print(f"{self.name} экипировал: {item.name} в слот {target_slot}")
        
        if self.current_hp > self.total_max_hp:
            self.current_hp = self.total_max_hp
            
        return old_item