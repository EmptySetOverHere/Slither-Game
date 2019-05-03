import json
import pygame
import numpy as np

try:
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
        #setting up grid as self.map
        self.square_color = color
        self.map = np.array([[x + xi + 1, y + yi + 1] for xi, x in enumerate(range(0, size[0], scale)) for yi, y in enumerate(range(0, size[1], scale))])
        self.size = (self.map[-1] + scale + 1).tolist()
        self.map = self.map.tolist()
        self.scale = scale + 1
        self.recycle_bin = [] #recycle_bin is a list of coordinates

    #draw grid on the screen
    def draw_grid(self, screen):

        screen.fill(self.square_color)
        for x in range(0, self.size[0], self.scale):
            pygame.draw.line(screen, (150, 150, 150), (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], self.scale):
            pygame.draw.line(screen, (150, 150, 150), (0, y), (self.size[0], y)) 


    def draw_snake(self, screen, snk_body, snk_color):
        for b in snk_body:
            #draw the snake body and update the map
            pygame.draw.rect(screen, snk_color, pygame.Rect(b[0], b[1], self.scale - 1, self.scale - 1))
            if b in self.recycle_bin:
                self.recycle_bin.remove(b)
        
        #padding the removed square
        if len(self.recycle_bin) >= 1:
            pygame.draw.rect(screen, self.square_color, pygame.Rect(self.recycle_bin[0][0], self.recycle_bin[0][1], self.scale - 1, self.scale - 1))
        self.recycle_bin = snk_body[:]
        

    def draw_food(self, screen, food_pos, food_color):
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], self.scale - 1, self.scale - 1))



    def get_map(self):
        return self.map



if __name__ == "__main__":
    mp = grid()
    print(mp.get_map()[:50])