import pygame
from classes.player import Player
from enemy import Enemy
import random
from classes.location import Location
from battle import BattleManager
from settings import *
from classes.level import Level

class Game:
    def __init__(self):

        pygame.init()
        self.player = Player()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('arial', 36)

        self.clock = pygame.time.Clock()

        self.current_location = Location((20, 30, 20), (600, 300, 50, 50), (380, 50, 50, 50))

        self.running = True
        self.game_state = 'MAP'
        self.current_battle = None

    def run(self):
        while self.running == True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == 'BATTLE':
                        self.current_battle.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == 'GAME_OVER':
                            self.player.stats.current_hp = self.player.stats.max_hp
                            self.enemies = [Enemy()]
                            self.game_state = 'MAP'
            self.screen.fill(BG_COLOR)

            if self.game_state == 'MAP':

                self.current_location.draw(self.screen)
                self.player.update()
                new_state = self.current_location.update(self.player)

                if new_state == 'BATTLE':
                    test_level = Level('Тестовая арена', [[Enemy()], [Enemy(), Enemy()]])
                    self.game_state = 'BATTLE'
                    self.current_battle = BattleManager(self.player, test_level) 
                    
                elif new_state == 'NEXT_LOC':
                    print("Телепортация в следующую комнату!")
                    self.player.rect.x = 400
                    self.player.rect.y = 500
                        
                self.player.draw(self.screen)

            elif self.game_state == 'BATTLE':
                self.screen.fill((0, 0, 0))
                self.current_battle.draw(self.screen)
                self.game_state = self.current_battle.update()

            elif self.game_state == 'GAME_OVER':
                self.screen.fill((100, 0, 0))
                game_over_text = self.font.render('Волосня поглотила вас...', True, (255, 255, 255))
                press_space = self.font.render('нажмите ПРОБЕЛ, чтобы продолжить', True, (255, 255, 255))
                self.screen.blit(press_space, (200, 200))
                self.screen.blit(game_over_text, (200, 300))


            pygame.display.flip()