import json
import os
from core import asset_manager
from components.item import Equipment, Consumable, Material, QuestItem

_items_database = {}

def init():
    global _items_database
    
    path = os.path.join(asset_manager.ROOT_DIR, 'assets', 'data', 'items.json')
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            _items_database = json.load(file)
        print(f"[УСПЕХ] Загружено {_items_database.__len__()} предметов из базы данных.")
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл базы данных предметов не найден: {path}")
    except json.JSONDecodeError:
        print(f"[ОШИБКА] Ошибка чтения JSON в файле: {path}")

def create_item(item_id: str):
    if item_id not in _items_database:
        print(f"[ПРЕДУПРЕЖДЕНИЕ] Предмет с ID '{item_id}' не найден в базе!")
        return None
        
    data = _items_database[item_id].copy()
    
    item_type = data.pop("type")
    
    if item_type == "Consumable":
        return Consumable(item_id=item_id, **data)
    elif item_type == "Equipment":
        return Equipment(item_id=item_id, **data)
    elif item_type == "Material":
        return Material(item_id=item_id, **data)
    elif item_type == "QuestItem":
        return QuestItem(item_id=item_id, **data)
    else:
        print(f"[ОШИБКА] Неизвестный тип предмета '{item_type}' у '{item_id}'")
        return None