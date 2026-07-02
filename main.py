from settings import *
import pygame
from classes.player import Player
import random
from battle import BattleManager
from enemy import Enemy

pygame.init()
player = Player()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont('arial', 36)

artifact_rect = pygame.Rect(600, 300, 20, 20)

clock = pygame.time.Clock()

enemies = []
enemies.append(Enemy( ))

artifacts_collected = 0

running = True
game_state = 'MAP'
current_battle = None

while running == True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'BATTLE':
                current_battle.handle_click(event.pos)
    screen.fill(BG_COLOR)

    if game_state == 'MAP':

        pygame.draw.rect(screen, (0, 0, 255), artifact_rect)
        player.update()

        for enemy in enemies:
            enemy.update(player)
            enemy.draw(screen)

            if player.rect.colliderect(enemy):
                game_state = 'BATTLE'
                current_battle = BattleManager(player, enemy)

        if player.rect.colliderect(artifact_rect):
            artifacts_collected += 1
            artifact_rect.x = random.randint(0, WIDTH - 20)
            artifact_rect.y = random.randint(0, HEIGHT - 20)
            print(f'Собрано волосиков: {artifacts_collected}')

        score_text = font.render(f'Волосиков: {artifacts_collected}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        player.draw(screen)

    elif game_state == 'BATTLE':
        screen.fill((0, 0, 0))
        current_battle.draw(screen)


    pygame.display.flip()



pygame.quit()