#!/usr/bin/python3
# coding: utf-8

import numpy as np
import random

class snake: 

    def __init__(self, grid_instance):
        self._map_ref = grid_instance
        self._color = (255, 255, 255)
        self._head_pos = random.choice(self._map_ref.get_map())
        self._status = True
        self._valid_directions = ["A", "D", "W", "S"]
        self._direction = None
        self._body = [self._head_pos]
        self._length = len(self._body)


    def move(self):
        
        self._head_pos = self._body[0][:]
        
        if self._direction == "A":
            self._head_pos = self._map_ref.get_neighbors(self._head_pos)["A"]
            self._valid_directions = ["S", "A", "W"]
        elif self._direction == "D":
            self._head_pos = self._map_ref.get_neighbors(self._head_pos)["D"]
            self._valid_directions = ["W", "D", "S"]
        elif self._direction == "W":
            self._head_pos = self._map_ref.get_neighbors(self._head_pos)["W"]
            self._valid_directions = ["A", "W", "D"]
        elif self._direction == "S":
            self._head_pos = self._map_ref.get_neighbors(self._head_pos)["S"]
            self._valid_directions = ["D", "S", "A"]

        if self._head_pos is None or self._head_pos in self._body[1:]:
            self._status = False
        else:
            self._status = True
            #update the entire body
            self._body.insert(0, self._head_pos[:])  
            self._body.pop()         
    
    
    def feed(self, food_instance):

        fd = food_instance
        if fd.pos == self._head_pos and self._direction:
            if self._length >= 2:
                vec = np.array(self._body[-1]) - np.array(self._body[-2])
                new_body = tuple((np.array(self._body[-1]) + vec).tolist()) 
                self._body.append(new_body)

            else:
                if self._direction == "W": new_body = self._map_ref.get_neighbors(self._head_pos)["S"]  
                elif self._direction == "A": new_body = self._map_ref.get_neighbors(self._head_pos)["D"]
                elif self._direction == "S": new_body = self._map_ref.get_neighbors(self._head_pos)["W"]
                elif self._direction == "D": new_body = self._map_ref.get_neighbors(self._head_pos)["A"]
                    
                self._body.append(new_body)

            self._length += 1
            fd.status = False
            
        
    def receive_signal(self, direction):
        if direction in self._valid_directions:
            self._direction = direction

    def get_body(self):
        return self._body[:]
    
    def get_color(self):
        return self._color[:]
    
    def check_status(self):
        return self._status
   
   
