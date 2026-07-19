class Level:
    def __init__(self, level_id: str, name: str, waves: list[list], 
                 xp_modifier: float, rewards: dict, special_conditions: dict):
        self.level_id = level_id
        self.name = name
        self.waves = waves
        self.xp_modifier = xp_modifier
        self.rewards = rewards
        self.special_conditions = special_conditions

        self.current_wave_index = 0

    def get_current_enemies(self) -> list:
        return self.waves[self.current_wave_index]

    def next_wave(self):
        self.current_wave_index += 1

    def is_completed(self) -> bool:
        return self.current_wave_index >= len(self.waves)