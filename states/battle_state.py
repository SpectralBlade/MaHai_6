from states.base_state import GameState
from states.battle import BattleManager

class BattleState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.battle_manager = None

    def enter(self, **kwargs):
        level = kwargs.get('level')
        self.battle_manager = BattleManager(self.game.profile, level)

    def handle_events(self, events):
        for event in events:
            if self.battle_manager:
                self.battle_manager.handle_event(event)

    def update(self):
        if not self.battle_manager:
            return
            
        result = self.battle_manager.update()
        
        if result == 'VICTORY':
            self.game.player.rect.x -= 60 
            self.game.change_state('VICTORY_SCREEN', level=self.battle_manager.level)
            
        elif result == 'GAME_OVER':
            self.game.change_state('GAME_OVER')

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.battle_manager:
            self.battle_manager.draw(screen)