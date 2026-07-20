from components.inventory import Inventory
from components.playable_character import PlayableCharacter
from core import item_manager, character_manager

class Profile:
    def __init__(self):
        self.gold = 100
        self.inventory = Inventory(capacity=20)
        
        self.roster: list[PlayableCharacter] = []  
        self.party: list[PlayableCharacter] = []  

        self.cleared_levels = set() 

        self._init_starting_items()

    def _init_starting_items(self):
        potion = item_manager.create_item('health_potion_01')
        if potion: self.inventory.add_item(potion, amount=5)
            
        sword = item_manager.create_item('rusty_sword')
        if sword: self.inventory.add_item(sword, amount=1)

    def choose_starter(self, character_id: str):
        hero = character_manager.create_character(character_id)
        if hero:
            self.roster.append(hero)
            self.party.append(hero)