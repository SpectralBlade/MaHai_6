class GameState:
    def __init__(self, game):
        self.game = game

    def enter(self, **kwargs):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass