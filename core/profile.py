from components.inventory import Inventory
from core import item_manager

class Profile:
    def __init__(self):
        self.inventory = Inventory(capacity=20)
        
        self.gold = 100
        self.party = []

        potion = item_manager.create_item('health_potion_01')
        if potion:
            self.inventory.add_item(potion, amount=5)
            
        sword = item_manager.create_item('rusty_sword')
        if sword:
            self.inventory.add_item(sword, amount=1)