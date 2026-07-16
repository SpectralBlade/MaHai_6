class Character:
    def __init__(self, name: str, max_hp: int, attack: int, resists: list = None, max_mana: int = 0):
        self.name = name

        self.max_hp = max_hp
        self.current_hp = max_hp

        self.max_mana = max_mana
        self.current_mana = max_mana

        self.attack = attack
        self.resists = resists if resists is not None else [] 

        self.active_status_effects = []

    def take_damage(self, damage_amount: int):
        self.current_hp -= damage_amount

        if self.current_hp < 0:
            self.current_hp = 0

        print(f'{self.name} получает {damage_amount} урона! Осталось {self.current_hp} здоровья')

    def apply_status_effect(self, effect):
        self.active_status_effects.append(effect)
        effect.on_apply(self)

    def update_status_effects(self):
        for effect in self.active_status_effects[:]:
            effect.on_turn_tick(self)
            if effect.duration <= 0:
                self.active_status_effects.remove(effect)