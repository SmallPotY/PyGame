# -*- coding:utf-8 -*-
import pygame


# Point class
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x

    def setx(self, x): self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y

    def sety(self, y): self.__y = y

    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
               ",Y:" + "{:.0f}".format(self.__y) + "}"


class BaseSprite(pygame.sprite.Sprite):
    x = 0
    y = 0

    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0  # 0下 1左 2右 3上
        self.moving = True  # 是否正在移动

    def load(self, filename, width, height, columns):
        """
        :param filename: 主精灵图文件
        :param width: 每帧宽度
        :param height: 每帧高度
        :param columns: 每行共多少帧
        """
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 0, 0, width, height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=60):
        # 根据 self.direction 确定播放哪一行的动画
        self.first_frame = self.direction * self.columns
        self.last_frame = self.first_frame + self.columns - 1
        if self.frame < self.first_frame:
            self.frame = self.first_frame

        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


class Man(BaseSprite):

    def move(self):
        if self.moving:
            if self.direction == 0:  # 0下 1左 2右 3上
                self.y += 5
            elif self.direction == 1:
                self.x -= 5
            elif self.direction == 2:
                self.x += 5
            elif self.direction == 3:
                self.y -= 5
