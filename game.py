import os
import pygame
import random
import json
import threading
import numpy as np
from collections import deque
from  pygame.locals import *

AI_MODE = False
Game_stage = 1
Game_Status = True

try:
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']

except Exception as e:
    print(e)
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
        self.body = deque([self.init_pos])
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
        if fd.pos == self.lead_pos:
            self.body.appendleft(self.lead_pos)
            self.length += 1
            fd.status = False
            print("Stage {}".format(Game_stage))
            
    def check_status(self):
        if self.body[0] in self.body[1:]:
            self.status = False
            return self.status
        elif self.body[0][0] >= scn_size[0] or self.body[0][0] < 0 or self.body[0][1] >= scn_size[1] or self.body[0][1] < 0:
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
        try:
            import AI
            snk_AI = AI.slitherAI()
        except Exception as e:
            print(e)
            exit(0)
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
            snk_AI.rectify()
            snk_AI.log_inputs(snk_1, apple)
            snk_AI.check_valid_ouputs(snk_1.body[0])
            snk_AI.brew()
            snk_1.input_buffer.append(snk_AI.vomit_output())
        
        snk_1.feed(apple)
        snk_1.move()
        apple.regenerate(position_set)
        obj_update(scn, snk_1, apple)
        pygame.display.update()
        Game_Status = snk_1.check_status()

        clk.tick(Game_stage + 18)

    pygame.quit()



main()