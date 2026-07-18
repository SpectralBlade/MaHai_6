from components.inventory import Inventory
from components.playable_character import PlayableCharacter
from core import item_manager

class Profile:
    def __init__(self):
        self.gold = 100
        self.inventory = Inventory(capacity=20)
        
        self.roster: list[PlayableCharacter] = [] 
        self.party: list[PlayableCharacter] = []   

        self._init_starting_profile()

    def _init_starting_profile(self):

        main_hero = PlayableCharacter(
            character_id="hero_01", 
            name="Spectrum", 
            max_hp=100, 
            attack=15, 
            max_mana=50
        )
        
        self.roster.append(main_hero)
        self.party.append(main_hero)

        potion = item_manager.create_item('health_potion_01')
        if potion: self.inventory.add_item(potion, amount=5)
            
        sword = item_manager.create_item('rusty_sword')
        if sword: self.inventory.add_item(sword, amount=1)