# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import math
import random

pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))

acc = [0, 0]
arrows = []

bad_timer = 100
bad_timer1 = 0
bad_guys = [[640, 100]]
health_value = 194

# 设置音乐
pygame.mixer.init()
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 加载角色 背景 物品 ......
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
bad_guy = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

keys = {
    'w': False,
    's': False,
    'a': False,
    'd': False
}
player_pos = [100, 100]

clock = pygame.time.Clock()

while True:
    bad_timer -= 1

    # 在屏幕绘制之前使用黑色填充
    screen.fill(0)

    # 往屏幕中添加元素
    for x in range(int(width / grass.get_width() + 1)):
        for y in range(int(height / grass.get_height() + 1)):
            screen.blit(grass, (x * 100, y * 100))

    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    if bad_timer == 0:
        bad_guys.append([640, random.randint(50, 430)])
        bad_timer = 100 - (bad_timer1 * 2)
        if bad_timer1 >= 35:
            bad_timer1 = 35
        else:
            bad_timer1 += 5
    index = 0
    for i in bad_guys:
        if i[0] < -64:
            bad_guys.pop(index)
        i[0] -= 7

        badrect = pygame.Rect(bad_guy.get_rect())
        badrect.top = i[1]
        badrect.left = i[0]
        if badrect.left < 64:
            hit.play()
            health_value -= random.randint(5, 20)
            bad_guys.pop(index)

        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                bad_guys.pop(index)
                arrows.pop(index1)
            index1 += 1
        index += 1
    for i in bad_guys:
        screen.blit(bad_guy, i)

    # 获取鼠标位置
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (player_pos[1] + 32), position[0] - (player_pos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerpos1 = (player_pos[0] - playerrot.get_rect().width / 2, player_pos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)

    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    # 6.5 - Draw health bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(health_value):
        screen.blit(health, (health1 + 8, 8))
    #
    # font = pygame.font.Font(None, 24)
    # survivedtext = font.render(
    #     str((90000 - pygame.time.get_ticks()) / 60000) + ":" + str((90000 - pygame.time.get_ticks()) / 1000 % 60).zfill(
    #         2), True, (0, 0, 0))
    # textRect = survivedtext.get_rect()
    # textRect.topright = [635, 5]
    # screen.blit(survivedtext, textRect)

    # 更新屏幕
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append(
                [math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32,
                 playerpos1[1] + 32])

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys['w'] = True
            elif event.key == K_a:
                keys['a'] = True
            elif event.key == K_s:
                keys['s'] = True
            elif event.key == K_d:
                keys['d'] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys['w'] = False
            elif event.key == K_a:
                keys['a'] = False
            elif event.key == K_s:
                keys['s'] = False
            elif event.key == K_d:
                keys['d'] = False

    if keys['w']:
        player_pos[1] -= 5
    elif keys['s']:
        player_pos[1] += 5
    if keys['a']:
        player_pos[0] -= 5
    elif keys['d']:
        player_pos[0] += 5

    clock.tick(70)
