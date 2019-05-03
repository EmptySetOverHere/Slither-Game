import numpy
import random

class food:
    
    def __init__(self, map): 
        #valid_points is in terms of a list comprizes of all valid points where can position food
        self.pos = random.choice(map)
        self.color = (255, 0, 0)
        self.status = True 

    def regenerate(self, map, snk_body):
        map = map[:]
        if self.status == False:
            for b in snk_body:
                map.remove(b)
            self.pos = random.choice(map)
            self.status = True