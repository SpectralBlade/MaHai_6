import pygame

class Level:
    def __init__(self, name: str, waves: list[list]):

        self.name = name
        self.waves = waves

        self.current_wave_index = 0

    def get_current_enemies(self) -> list:
        return self.waves[self.current_wave_index]

    def next_wave(self):
        self.current_wave_index += 1

    def is_completed(self) -> bool:
        return self.current_wave_index >= len(self.waves)