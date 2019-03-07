# -*- coding:utf-8 -*-
import pygame
import setting
from Map import Map
from BaseSprite import BaseSprite,Man

_map = Map('map.xls')

pygame.init()
screen = pygame.display.set_mode((_map.width, _map.height), 0, 0)
pygame.display.set_caption(setting.TITLE)
framerate = pygame.time.Clock()

man = Man(screen)
man.load("resources/man_1.png", 25, 25, 3)
group = pygame.sprite.Group()
group.add(man)

while True:
    framerate.tick(setting.CLOCK)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()

    screen.fill((255, 255, 255))

    for i in _map.map_view:
        _map.rect(screen, i)
    man.move()
    group.update(ticks)
    group.draw(screen)
    pygame.display.update()
