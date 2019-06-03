#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os 
import pygame
from threading import Thread
from pygame.locals import *
pygame.init()

try:
    from bin import Grid, Snake, Food, AI
    
except Exception as e:
    print(e)
    exit(0)

AI_MODE = True

class SnakeGame:

    def __init__(self):
        
        self.ai_path = None
        self.grd = Grid.grid()
        self.snk = Snake.snake(self.grd.get_map(), self.grd.get_scale())
        self.apple = Food.food(self.grd.get_map())
        
        self.grd.receive_food(self.apple)
        self.grd.receive_snk(self.snk)
        
        if AI_MODE:
            self.aiInstance = AI.brutal_ai(self.grd)
        else:
            self.aiInstance = None

    def run(self):

        #initializing the game settings
        scn = pygame.display.set_mode(self.grd.get_size())
        clk = pygame.time.Clock()
        self.grd.draw_grid(scn)

        
        while True:

            if self.aiInstance is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        key_input = chr(event.key).capitalize()
                        self.snk.receive_signal(key_input)
                        
            elif self.ai_path:
                
                self.snk.receive_signal(self.ai_path[-1])
                self.ai_path.pop()
                
            else:
                self.ai_path = self.aiInstance.get_path()
                
                
            self.snk.move()
            self.snk.feed(self.apple)
            self.apple.regenerate(self.grd.get_map(), self.snk.body)

            Game_Status = self.snk.check_status(self.grd.get_obstacles())
            if Game_Status is True:
                self.grd.draw_snake(scn, self.snk.body, self.snk.head_color, self.snk.body_color)
                self.grd.draw_food(scn, self.apple.pos, self.apple.color)
                pygame.display.update()
            else:
                print("Game Over")
                break

            clk.tick(15)
                

        pygame.quit()
        


if __name__ == "__main__":
    
    while True:
        game = SnakeGame()
        game.run()
