class Effect:
    def __init__(self, effect_type: str, value: int, stat: str = None, duration: int = 0, **kwargs):
        self.type = effect_type     
        self.value = value          
        self.stat = stat             
        self.duration = duration       
        self.extra_data = kwargs      

    def apply(self, user, target):
        if self.type == "heal":
            target.current_hp = min(target.current_hp + self.value, target.max_hp)
            print(f"{target.name} восстановил {self.value} ХП!")
            
        elif self.type == "apply_buff":
            buff = StatusEffect(
                name=f"Бафф {self.stat}",
                stat_to_modify=self.stat,
                modifier=self.value,
                duration=self.duration
            )
            target.apply_status_effect(buff)
            
        elif self.type == "apply_debuff" and self.extra_data.get("status_name") == "poison":
            poison = PoisonEffect(
                damage=self.extra_data.get("damage_per_turn", 5),
                duration=self.duration
            )
            target.apply_status_effect(poison)


class StatusEffect:
    def __init__(self, name: str, stat_to_modify: str, modifier: int, duration: int):
        self.name = name
        self.stat_to_modify = stat_to_modify
        self.modifier = modifier
        self.duration = duration
        self.is_applied = False

    def on_apply(self, character):
        if not self.is_applied:
            current_val = getattr(character, self.stat_to_modify, 0)
            setattr(character, self.stat_to_modify, current_val + self.modifier)
            self.is_applied = True
            print(f"✨ На {character.name} наложен бафф: {self.name} (+{self.modifier} {self.stat_to_modify}) на {self.duration}х.")

    def on_turn_tick(self, character):
        self.duration -= 1
        if self.duration <= 0:
            self.on_remove(character)

    def on_remove(self, character):
        if self.is_applied:
            current_val = getattr(character, self.stat_to_modify, 0)
            setattr(character, self.stat_to_modify, current_val - self.modifier)
            self.is_applied = False
            print(f"Действие баффа {self.name} на {character.name} закончилось.")


class PoisonEffect:
    def __init__(self, damage: int, duration: int):
        self.name = "Отравление"
        self.damage = damage
        self.duration = duration

    def on_apply(self, character):
        print(f"{character.name} отравлен на {self.duration} ходов!")

    def on_turn_tick(self, character):
        character.take_damage(self.damage)
        self.duration -= 1

    def on_remove(self, character):
        print(f"Эффект отравления на {character.name} прошел.")