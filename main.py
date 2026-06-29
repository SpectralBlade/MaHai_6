from settings import *
import pygame
from player import Player

pygame.init()
player = Player()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

running = True

while running == True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BG_COLOR)
    player.update()
    player.draw(screen)
    pygame.display.flip()

pygame.quit()