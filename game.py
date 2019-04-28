__author__ = "SiSheng"

import os
import pygame
import random
import json
import threading
import numpy as np
import pickle
from AI import *
from collections import deque
from  pygame.locals import *

AI_MODE = True
Game_stage = 1
Game_Status = True

try:
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']
    
    with open("AIParameters.pickle", "rb") as p:
        hidden_layers = pickle.load(p)
        output_layer = pickle.load(p)
        print(hidden_layers)
        print(output_layer)
    
    with open("AIParameters.pickle", "wb") as p:
        p.truncate(0)


except Exception as e:
    raise(e)
    exit(0)


class food:

    def __init__(self, positions): 
        #valid_points is in terms of a list comprizes of all valid points where can position food
        self.pos = np.array(random.choice(positions))
        self.color = (255, 0, 0)
        self.status = True 

    def regenerate(self, positions):
        if self.status == False:
            self.pos = np.array(random.choice(positions))
            self.status = True
            global Game_stage
            Game_stage += 1
            

class snake: 

    def __init__(self, positions, snk_AI = None):
        self.color = (255, 255, 255)
        self.init_pos = np.array(random.choice(positions))
        self.status = True

        # initialize input buffer with two placeholders
        # input buffer takes in the character input from keyboard
        self.input_buffer = deque(["p", "p"]) 

        self.direction = ""
        self.body = [self.init_pos]
        self.length = len(self.body)
        self.lead_pos = self.init_pos

    def move(self, mode = 'n'):

        # n is the normal mode whereas p is the premove mode
        # move the head only

        self.direction = self.input_buffer[-1]
        if ((self.input_buffer[-1] == "A" and self.input_buffer[-2] == "D") or 
        (self.input_buffer[-1] == "D" and self.input_buffer[-2] == "A") or 
        (self.input_buffer[-1] == "W" and self.input_buffer[-2] == "S") or
        (self.input_buffer[-1] == "S" and self.input_buffer[-2] == "W")):
            self.input_buffer.pop()

        elif self.direction == "A":
            self.lead_pos = self.body[0] + np.array([-scn_scale, 0])
        elif self.direction == "D":
            self.lead_pos = self.body[0] + np.array([scn_scale, 0])
        elif self.direction == "W":
            self.lead_pos = self.body[0] + np.array([0, -scn_scale])
        elif self.direction == "S":
            self.lead_pos = self.body[0] + np.array([0, scn_scale])
        elif self.direction == "p":
            pass
        else:
            self.input_buffer.pop()

        #update the entire body
        if mode == 'p':
            return self.lead_pos
        elif mode == 'n':
            if len(self.input_buffer) > 2:
                self.input_buffer.popleft()

            for i in range(1, self.length):
                self.body[-i] = self.body[-i-1]
            self.body[0] = self.lead_pos            

    def feed(self, fd):
        self.move('p') #check its position before moving
        if fd.pos[0] == self.lead_pos[0] and fd.pos[1] == self.lead_pos[1]:
            self.body.insert(0, self.lead_pos)
            self.length += 1
            fd.status = False
            print("Stage {}".format(Game_stage))
            
    def check_status(self):
        for body_seg in self.body[1:]:
            if self.body[0][0] == body_seg[0] and self.body[0][1] == body_seg[1]:
                self.status = False
                return self.status
            
        if self.body[0][0] >= scn_size[0] or self.body[0][0] < 0 or self.body[0][1] >= scn_size[1] or self.body[0][1] < 0:
            self.status = False 
            return self.status

        else:
            return True


def obj_update(screen, *objects):
    #draw the ojects on the screen
    for obj in objects:
        if isinstance(obj, snake):
            for body_seg in obj.body:
                pygame.draw.rect(screen, obj.color, pygame.Rect(body_seg[0], body_seg[1], scn_scale, scn_scale))

        elif isinstance(obj, food):
            pygame.draw.rect(screen, obj.color, pygame.Rect(obj.pos[0], obj.pos[1], scn_scale, scn_scale))


def event_handler(snk_instance):
    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    key_input = chr(event.key).capitalize()
                    snk_instance.input_buffer.append(key_input)

        except:
            break



def main():

    global Game_Status
    pygame.init()
    scn = pygame.display.set_mode(scn_size)

    position_set = [(x, y) for x in range(0, scn_size[0], scn_scale) for y in range(0, scn_size[1], scn_scale)]

    snk_1 = snake(position_set)
    apple = food(position_set)

    clk = pygame.time.Clock()

    if AI_MODE:
        snk_AI = slitherAI(hidden_layers=hidden_layers, output_layer=output_layer)
    else:
        listen_event = threading.Thread(target=event_handler, args=(snk_1,))
        listen_event.start()


    while Game_Status is True:

        #render scn background
        scn.fill((50, 50, 50))
        for x in range(0, scn_size[0], scn_scale):
            pygame.draw.line(scn, (150, 150, 150), (x, 0), (x, scn_size[1]))
        for y in range(0, scn_size[1], scn_scale):
            pygame.draw.line(scn, (150, 150, 150), (0, y), (scn_size[0], y)) 

        #game process
        if AI_MODE:
            snk_AI.log_inputs(snk_1.body, [apple.pos])
            snk_AI.brew()
            snk_1.input_buffer.append(snk_AI.vomit_output())
        
        snk_1.feed(apple)
        snk_1.move()
        apple.regenerate(position_set)
        obj_update(scn, snk_1, apple)
        pygame.display.update()
        Game_Status = snk_1.check_status()

        if AI_MODE:
            snk_AI.propagate_backward(snk_1.body[0], apple.pos)

        clk.tick(Game_stage + 10)


    snk_AI.save_network()
    pygame.quit()



main()