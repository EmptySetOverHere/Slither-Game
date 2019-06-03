#!/usr/bin/python3
# coding: utf-8

import json
import pygame
import numpy as np

try:
    from bin import Food, Snake
    
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']
        scn_background_color = settings['scn_color']

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
        self._snk_tracker = [] #snk_tracker is a list of coordinates

        self._reshaped_map = self._map.reshape((int(ratio[0]), int(ratio[1]), 2))
        self._scale = scale + 1
        self._obstacle_stack = (self._reshaped_map[0, :] - np.array([self._scale, 0])).tolist() + (self._reshaped_map[:, 0] - np.array([0, self._scale])).tolist() + (self._reshaped_map[int(ratio[0]) - 1 , :] + np.array([self._scale, 0])).tolist() + (self._reshaped_map[:, int(ratio[1]) - 1] + np.array([0, self._scale])).tolist() 
        self._obstacle_stack = [tuple(each) for each in self._obstacle_stack]
        
        self._map = [tuple(each) for each in self._map.tolist()]
        
        
    #draw grid on the screen
    def draw_grid(self, screen):
        
        screen.fill(self._square_color)
        for x in range(0, self._size[0], self._scale):
            pygame.draw.line(screen, (150, 150, 150), (x, 0), (x, self._size[1]))
        for y in range(0, self._size[1], self._scale):
            pygame.draw.line(screen, (150, 150, 150), (0, y), (self._size[0], y)) 


    def draw_snake(self, screen, snk_body, snk_head_color, snk_body_color):
        
        pygame.draw.rect(screen, snk_head_color, pygame.Rect(snk_body[0][0], snk_body[0][1], self._scale - 1, self._scale - 1))
        if snk_body[0] in self._snk_tracker:
            self._snk_tracker.remove(snk_body[0])
        
        for b in snk_body[1:]:
            #draw the snake body and update the map
            pygame.draw.rect(screen, snk_body_color, pygame.Rect(b[0], b[1], self._scale - 1, self._scale - 1))
            if b in self._snk_tracker:
                self._snk_tracker.remove(b)
                
            if b in self._obstacle_stack:
                self._obstacle_stack.remove(b)
    
                
        #padding the removed square
        if len(self._snk_tracker) >= 1:
            pygame.draw.rect(screen, self._square_color, pygame.Rect(self._snk_tracker[0][0], self._snk_tracker[0][1], self._scale - 1, self._scale - 1))
        
        try:
            self._obstacle_stack += snk_body[1:]
            for square in self._snk_tracker:
                self._obstacle_stack.remove(square)
        except:
            pass

        self._snk_tracker = snk_body[:]

    def draw_food(self, screen, food_pos, food_color):
        
        self.food_pos = food_pos
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], self._scale - 1, self._scale - 1))

    def receive_snk(self, snk_instance):
        self._snk = snk_instance
        
    def receive_food(self, food_instance):
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
        return self._snk.body[0][:]
    
    def get_food_pos(self):
        return self._food.pos[:]


if __name__ == "__main__":
    mp = grid()
    print(mp.get_obstacles())