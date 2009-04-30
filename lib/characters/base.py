'''
Base class for characters
'''

import os.path
import math
import random
from .squirtle import SVG

class Character(object):
    ''' A generic GOMFL character '''

    name = "Target"

    # Look and feel
    LEFT = 'left'
    RIGHT = 'right'
    DEAD = 'dead'
    left=None
    right=None
    dead=None
    curr_view = LEFT 
    is_drawn = False

    # The scaling size should be related to the y position
    scale=0.3

    # Speed and strenght options
    speed=1
    speed_multiply=1
    strength=1

    # screen position defaults and setup
    ymax=300
    ymin=275
    xmax=775
    xmin=50
 
    def __init__(self):
        # What path to take and path options
        self.x = random.randint(self.xmin, self.xmax)
        self.y = random.randint(self.ymin, self.ymax)
        self.attack_path=self._vector()
        #self.x = 400 
        #self.y = 400
        
    def _vector(self):
        """
        Plot course
        """
        var_pos=[]
        x_pos=self.x
        y_pos=self.y
            
        if self.x < 75:
            #Move diag left to righ
            for i in range(1,800):
                x_pos += 1
                y_pos -= 1
                var_pos.append([x_pos,y_pos])
            return var_pos
                
        if self.x > 725:
            #Move diag left to righ
            for i in range(1,800):
                x_pos -= 1
                y_pos -= 1
                var_pos.append([x_pos,y_pos])
            return var_pos
            
        x_var = 5 
        counter = 0
        for i in range(1,800):
            y_pos -= 1
            
            if counter < x_var:
                x_pos += 1
                counter += 1
            
            if counter == 0:
                x_pos -= 1
                counter -= 1
                
            var_pos.append([x_pos,y_pos])
        return var_pos

    def move(self):
        try:
            delta = self.attack_path.pop(0)
            self.x = delta[0]
            self.y = delta[1]
        except IndexError:
            pass # no more path

    def draw(self):
        getattr(self, self.curr_view).draw(self.x, self.y, angle=0, scale=self.scale)


def create_svg(file_name, anchor_x='center', anchor_y='bottom'):
    return SVG(
        os.path.join('resources', file_name),
        anchor_x=anchor_x,
        anchor_y=anchor_y)
