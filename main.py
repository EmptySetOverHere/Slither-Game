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
        self.snk = Snake.snake(self.grd)
        self.apple = Food.food(self.grd.get_map())
        
        self.grd.locate_food(self.apple)
        self.grd.locate_snk(self.snk)
        
        if AI_MODE:
            self.aiInstance = AI.brutal_ai(self.grd)
        else:
            self.aiInstance = None
            
            
    def pause(self):
        
        start = True
        while start:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                    elif event.type == pygame.KEYDOWN:
                        if chr(event.key) == 'p':
                            start = False            
                if pygame.mouse.get_pressed()[0]:
                    print(f'Mouse Position: {pygame.mouse.get_pos()}')
            except:
                pass
        

    def run(self):

        #initializing the game settings
        scn = pygame.display.set_mode(self.grd.get_size())
        clk = pygame.time.Clock()
        self.grd.draw_grid(scn)

        
        while True:

            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    
                    if chr(event.key) == 'p':
                        self.pause()
                    
                    if self.aiInstance is None:
                    
                        key_input = chr(event.key).capitalize()
                        self.snk.receive_signal(key_input)
                        
            if self.ai_path and self.aiInstance:
                
                self.snk.receive_signal(self.ai_path.pop())
                
            elif self.aiInstance:
                
                self.ai_path = self.aiInstance.get_path()
                if self.ai_path:
                    self.snk.receive_signal(self.ai_path.pop())
                else:
                    break
                
                
            self.snk.move()
            self.snk.feed(self.apple)
            self.apple.regenerate(self.grd.get_map(), self.snk.get_body())

            Game_Status = self.snk.check_status()
            if Game_Status is True:
                self.grd.draw_snake(scn, self.snk.get_body(), self.snk.get_color())
                self.grd.draw_food(scn, self.apple.pos, self.apple.color)
                pygame.display.update()
            else:
                print("Game Over")
                break

            clk.tick(self.grd.get_refresh_rate())
                

        pygame.quit()
        


if __name__ == "__main__":
    
    while True:
        game = SnakeGame()
        game.run()
