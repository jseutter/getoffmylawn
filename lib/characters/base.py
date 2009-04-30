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
    xmax=400
    xmin=200
 
    def __init__(self):
        # What path to take and path options
        self.attack_path=self._vector()
        # self.x = random.randint(self.xmin, self.xmax)
        # self.y = random.randint(self.ymin, self.ymax)
        self.x = 400 
        self.y = 400

    def _path1(self):
        """
        Path 1 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append((int(math.sin(seq)*-30), random.randint(0,2)))
        return var_pos
        
    def _path2(self):
        """
        Path 2 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append((int(math.cos(seq)*50), random.randint(0,2)))
        return var_pos
       
    def _path3(self):
        """
        Path 3 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append((int(math.cos(seq)*35), random.randint(0,2)))
        return var_pos
        
    def _vector(self):
        """
        Plot course
        """
        vector_opt=(self._path1,self._path2,self._path3)     
        c = random.randint(0,(len(vector_opt)-1))
        return vector_opt[c]()

    def move(self):
        try:
            delta = self.attack_path.pop()
            self.x -= delta[0]
            self.y -= delta[1]
        except IndexError:
            pass # no more path

    def draw(self):
        getattr(self, self.curr_view).draw(self.x, self.y, angle=0, scale=self.scale)


def create_svg(file_name, anchor_x='center', anchor_y='bottom'):
    return SVG(
        os.path.join('resources', file_name),
        anchor_x=anchor_x,
        anchor_y=anchor_y)
