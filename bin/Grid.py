#!/usr/bin/python3
# coding: utf-8

import json
import pygame
import numpy as np
from copy import deepcopy

try:
    from bin import Food, Snake
    
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']
        scn_background_color = settings['scn_color']
        Refresh_Rate = settings['Refresh_Rate']

except Exception as e:
    print(e)
    exit(0)


class grid:

    #defining the property of a grid
    def __init__(self, size = scn_size, scale = scn_scale, color = scn_background_color):

        try:
            #check whether the screen parameters are legal or not
            ratio = [size[0] / scale, size[1] / scale]
            if int(ratio[0]) - ratio[0] != 0 or int(ratio[1]) - ratio[1] != 0:
                raise ValueError("The ratio of screen size to its scale can not be an non-integer value")

            if len(color) != 3:
                raise ValueError("Illegal Color Value: color should be in terms of rgb values i.e. [255, 255, 255]")

        except Exception as e:
            print(e)
            print("Please ensure your parameters in game_config.json file are legal")
            exit(0)

        #set imported values as property
        #initializing grid as self.map
        self._square_color = color
        self._map = np.array([[x + xi + 1, y + yi + 1] for xi, x in enumerate(range(0, size[0], scale)) for yi, y in enumerate(range(0, size[1], scale))])
        self._size = (self._map[-1] + scale + 1).tolist()
        
        self._reshaped_map = self._map.reshape((int(ratio[0]), int(ratio[1]), 2))
        self._scale = scale + 1
        self._obstacle_stack = (self._reshaped_map[0, :] - np.array([self._scale, 0])).tolist() + (self._reshaped_map[:, 0] - np.array([0, self._scale])).tolist() + (self._reshaped_map[int(ratio[0]) - 1 , :] + np.array([self._scale, 0])).tolist() + (self._reshaped_map[:, int(ratio[1]) - 1] + np.array([0, self._scale])).tolist() 
        self._obstacle_stack = tuple(tuple(each) for each in self._obstacle_stack)
        self._map = [tuple(each) for each in self._map.tolist()]
        
        self._direction_dict = {"A":np.array([-self._scale, 0]), "D":np.array([self._scale, 0]), "W":np.array([0, -self._scale]), "S":np.array([0, self._scale])}
        self._adjacent_node = dict()
        
        for node in self._map:
            neighbors = dict()
            for key, value in self._direction_dict.items():
                neighbor = tuple(node + value)
                if neighbor in self._obstacle_stack:
                    neighbors[key] = None
                else:
                    neighbors[key] = neighbor
            self._adjacent_node[node] = neighbors
        
        self._snk_tracker = [] # record the previous version of snake
                    
    #draw grid on the screen
    def draw_grid(self, screen):
        
        screen.fill(self._square_color)
        for x in range(0, self._size[0], self._scale):
            pygame.draw.line(screen, (150, 150, 150), (x, 0), (x, self._size[1]))
        for y in range(0, self._size[1], self._scale):
            pygame.draw.line(screen, (150, 150, 150), (0, y), (self._size[0], y)) 


    def draw_snake(self, screen, snk_body, snk_color):
        
        for cell in self._snk_tracker:
            pygame.draw.rect(screen, self._square_color, pygame.Rect(cell[0], cell[1], self._scale - 1, self._scale - 1))
        
        for cell in snk_body:
            pygame.draw.rect(screen, snk_color, pygame.Rect(cell[0], cell[1], self._scale - 1, self._scale - 1))

                
        self._snk_tracker = snk_body[:]


    def draw_food(self, screen, food_pos, food_color):
        
        self.food_pos = food_pos
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], self._scale - 1, self._scale - 1))

    def get_neighbors(self, node):
        return deepcopy(self._adjacent_node[node])

    def locate_snk(self, snk_instance):
        self._snk = snk_instance
        
    def locate_food(self, food_instance):
        self._food = food_instance
    
    def get_map(self):
        return self._map
    
    def get_scale(self):
        return self._scale
    
    def get_size(self):
        return self._size
    
    def get_obstacles(self):
        return self._obstacle_stack

    def get_snk_pos(self):
        return self._snk._body[0][:]
    
    def get_snk_body(self):
        return self._snk._body[:]
    
    def get_food_pos(self):
        return self._food.pos[:]

    def get_refresh_rate(self):
        return Refresh_Rate
    
    
if __name__ == "__main__":
    import sys
    mp = grid()
    print(mp._adjacent_node[(52, 52)])