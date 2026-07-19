import json
import os
from core import asset_manager
from components.playable_character import PlayableCharacter

_characters_database = {}

def init():
    global _characters_database
    path = os.path.join(asset_manager.ROOT_DIR, 'assets', 'data', 'characters.json')
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            _characters_database = json.load(file)
        print(f"Загружено {_characters_database.__len__()} персонажей из базы.")
    except Exception as e:
        print(f"Ошибка загрузки characters.json: {e}")

def create_character(character_id: str) -> PlayableCharacter | None:
    if character_id not in _characters_database:
        print(f"Персонаж '{character_id}' не найден!")
        return None
        
    data = _characters_database[character_id].copy()
    
    return PlayableCharacter(character_id=character_id, **data)