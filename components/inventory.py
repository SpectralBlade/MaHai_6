from __future__ import annotations

class InventorySlot:
    def __init__(self):
        self.item = None
        self.quantity = 0

    @property
    def is_empty(self) -> bool:
        return self.item is None

    def clear(self):
        self.item = None
        self.quantity = 0


class Inventory:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.slots = [InventorySlot() for _ in range(capacity)]

    def add_item(self, item_to_add, amount: int = 1) -> int:
        leftover = amount

        for slot in self.slots:
            if not slot.is_empty and slot.item.item_id == item_to_add.item_id:
                space_in_slot = slot.item.max_stack - slot.quantity

                if space_in_slot > 0:
                    if space_in_slot >= leftover:
                        slot.quantity += leftover
                        return 0
                    else:
                        slot.quantity += space_in_slot
                        leftover -= space_in_slot

        if leftover > 0:
            for slot in self.slots:
                if slot.is_empty:
                    slot.item = item_to_add

                    if leftover <= item_to_add.max_stack:
                        slot.quantity = leftover
                        return 0
                    else:
                        slot.quantity = item_to_add.max_stack
                        leftover -= item_to_add.max_stack

        return leftover

    def remove_item(self, item_id: str, amount: int = 1) -> bool:
        total_found = sum(slot.quantity for slot in self.slots if not slot.is_empty and slot.item.item_id == item_id)

        if total_found < amount:
            return False

        remaining_to_remove = amount
        for slot in reversed(self.slots):
            if not slot.is_empty and slot.item.item_id == item_id:
                if slot.quantity > remaining_to_remove:
                    slot.quantity -= remaining_to_remove
                    return True
                else:
                    remaining_to_remove -= slot.quantity
                    slot.clear()

                if remaining_to_remove <= 0:
                    break

        return True