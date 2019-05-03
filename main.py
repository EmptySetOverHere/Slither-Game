#!/usr/bin/python3
# coding: utf-8
import os 
import pygame
import threading
from pygame.locals import *

try:
    from bin import Grid
    from bin import Snake
    from bin import Food
except Exception as e:
    print(e)
    exit(0)




def game():

    #initializing the game settings
    pygame.init()
    grd = Grid.grid()
    scn = pygame.display.set_mode(grd.size)
    clk = pygame.time.Clock()
    grd.draw_grid(scn)

    snk = Snake.snake(grd.map, grd.scale)
    apple = Food.food(grd.map)


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                key_input = chr(event.key).capitalize()
                snk.receive_signal(key_input)

        
        snk.move()
        snk.feed(apple)
        apple.regenerate(grd.map, snk.body)

        Game_Status = snk.check_status(grd.map)
        if Game_Status is True:
            grd.draw_snake(scn, snk.body, snk.color)
            grd.draw_food(scn, apple.pos, apple.color)
            pygame.display.update()
        else:
            break

        clk.tick(15)
    
    pygame.quit()


if __name__ == "__main__":
    game()