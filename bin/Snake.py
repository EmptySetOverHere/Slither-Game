#!/usr/bin/python3
# coding: utf-8

import numpy as np
import random

class snake: 

    def __init__(self, map, scn_scale):
        self.head_color = (255, 255, 255)
        self.body_color = (0, 255, 0)
        self.head_pos = random.choice(map)
        self.status = True
        self.valid_directions = ["A", "D", "W", "S"]
        self.direction = ""
        self.body = [self.head_pos]
        self.length = len(self.body)
        self.direction_vectors = {"A":np.array([-scn_scale, 0]), "D":np.array([scn_scale, 0]), "W":np.array([0, -scn_scale]), "S":np.array([0, scn_scale])}


    def move(self):
       
        self.head_pos = np.array(self.body[0])

        if self.direction == "A":
            self.head_pos += self.direction_vectors["A"]
            self.valid_directions = ["S", "A", "W"]
        elif self.direction == "D":
            self.head_pos += self.direction_vectors["D"]
            self.valid_directions = ["W", "D", "S"]
        elif self.direction == "W":
            self.head_pos += self.direction_vectors["W"]
            self.valid_directions = ["A", "W", "D"]
        elif self.direction == "S":
            self.head_pos += self.direction_vectors["S"]
            self.valid_directions = ["D", "S", "A"]

        #update the entire body
        self.head_pos = tuple(self.head_pos.tolist())
        if self.length > 1:
            for i in range(1, self.length):
                self.body[-i] = self.body[-i-1]
        self.body[0] = self.head_pos[:]           



    def feed(self, food_instance):

        fd = food_instance
        if fd.pos == self.head_pos:
            if self.length >= 2:
                vec = np.array(self.body[-1]) - np.array(self.body[-2])
                new_body = tuple((np.array(self.body[-1]) + vec).tolist()) 
                self.body.append(new_body)

            else:
                vec = - self.direction_vectors[self.direction]
                new_body = tuple((np.array(self.head_pos) + vec).tolist()) 
                self.body.append(new_body)

            self.length += 1
            fd.status = False
            
    

    def check_status(self, obstacles):
        
        if self.head_pos in obstacles:
            self.status = False
            return self.status
        
        else:
            return True
        

    def receive_signal(self, direction):
        if direction in self.valid_directions:
            self.direction = direction

   