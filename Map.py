# -*- coding:utf-8 -*-
import pygame
import xlrd
import setting


class Map:

    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.filename = filename
        self.map_view = None
        self.position_type = {}
        self.cols = 0
        self.rows = 0
        self.frame_width = setting.FRAME_WIDTH
        self.frame_height = setting.FRAME_HEIGHT
        self.load_map()

    def load_map(self):
        wb = xlrd.open_workbook(self.filename)
        tmp = wb.sheet_by_index(0)
        self.rows = tmp.nrows
        self.cols = tmp.ncols

        self.width = self.cols * self.frame_width
        self.height = self.rows * self.frame_height

        tmp_list = []
        for r in range(self.rows):
            for c in range(self.cols):
                position = {
                    'r': r,
                    'c': c,
                    'type': tmp.cell(r, c).value
                }
                key = '{},{}'.format(r, c)
                self.position_type[key] = tmp.cell(r, c).value
                tmp_list.append(position)
        self.map_view = tmp_list

    @staticmethod
    def rect(window, location):
        cell_width = setting.FRAME_WIDTH
        cell_height = setting.FRAME_HEIGHT
        left = location['c'] * cell_width
        top = location['r'] * cell_height

        color = (255, 255, 255)

        if location['type'] == 1:
            color = (100, 0, 0)
        elif location['type'] == 2:
            color = (0, 100, 0)
        pygame.draw.rect(
            window, color,
            (left, top, cell_width, cell_height)
        )
