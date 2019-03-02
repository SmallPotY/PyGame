# -*- coding:utf-8 -*-
import pygame
import random


class Point:
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Point(row=self.row, col=self.col)


# 初始化
pygame.init()
W = 800
H = 600

ROW = 60
COL = 80

# 设置大小 标题
size = (W, H)
window = pygame.display.set_mode(size)
pygame.display.set_caption('贪吃蛇')
bg_color = (255, 255, 255)

# 定义坐标
head = Point(row=int(ROW / 2), col=int(COL / 2))
head_color = (0, 128, 128)
food_color = (111, 11, 111)
snakes_color = (90, 90, 90)
# 移动方向
direct = 'left'

snakes = [
    Point(row=head.row, col=head.col + 1),
    Point(row=head.row, col=head.col + 2),
    Point(row=head.row, col=head.col + 3)
]


def gen_food():
    while True:
        pos = Point(row=random.randint(0, ROW - 1), col=random.randint(0, COL - 1))
        is_coll = False
        if head.row == pos.row and head.col == pos.col:
            is_coll = True

        for s in snakes:
            if s.col == pos.col and s.row == pos.row:
                is_coll = True
                break
        if not is_coll:
            break
    return pos


food = gen_food()


def rect(point, color):
    cell_width = W / COL
    cell_height = H / ROW
    left = point.col * cell_width
    top = point.row * cell_height

    pygame.draw.rect(
        window, color,
        (left, top, cell_width, cell_height)
    )


# 游戏循环
game_quit = True
clock = pygame.time.Clock()
while game_quit:

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 273 or event.key == 119:
                if direct != 'down':
                    direct = 'up'
            elif event.key == 274 or event.key == 115:
                if direct != 'up':
                    direct = 'down'
            elif event.key == 276 or event.key == 94:
                if direct != 'right':
                    direct = 'left'
            elif event.key == 275 or event.key == 100:
                if direct != 'left':
                    direct = 'right'

    # 吃东西
    eat = (head.row == food.row and head.col == food.col)

    if eat:
        food = gen_food()

        # 移动
    snakes.insert(0, head.copy())
    if not eat:
        snakes.pop()

    if direct == 'left':
        head.col -= 1
    elif direct == 'right':
        head.col += 1
    elif direct == 'up':
        head.row -= 1
    elif direct == 'down':
        head.row += 1

    dead = False
    if head.col < 0 or head.row < 0 or head.col >= COL or head.row >= ROW:
        dead = True

    for snake in snakes:
        if head.col == snake.col and head.row == snake.row:
            dead = True
        break

    if dead:
        game_quit = False

    # 渲染背景
    pygame.draw.rect(window, (255, 255, 255), (0, 0, W, H))

    # 蛇头
    rect(head, head_color)
    # 身体
    for snake in snakes:
        rect(snake, snakes_color)
    # 食物
    rect(food, food_color)

    # flip() 让出控制权
    pygame.display.flip()

    # 设置帧频
    clock.tick(20)
