'''
Base class for characters
'''
import math
import random

class Character(object):
    ''' A generic GOMFL character '''

    name = "Target"
    svg = "crosshair.svg"

    # Look and feel
    left=None
    right=None
    dead=None

    # The scaling size should be related to the y position
    scale=1

    # Speed and strenght options
    speed=1
    speed_multiply=1
    strength=1

    # screen position defaults and setup
    ymax=300
    ymin=275
    xmax=790
    xmin=10
    ystart = random.randint(ymin,ymax)
    xstart = random.randint(xmin,xmax)
    xloc=0
    yloc=0
 
    def __init__(self):
        # What path to take and path options
        self.attack_path=self._vector()

    def _path1(self):
        """
        Path 1 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append(int(math.sin(seq) * 10))
        return var_pos
        
    def _path2(self):
        """
        Path 2 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append(int(math.cos(seq) * 10))
        return var_pos
       
    def _path3(self):
        """
        Path 3 course
        """
        var_pos=[]
        for seq in range(1,800):
            var_pos.append(int(math.cos(seq) * 10))
        return var_pos
        
    def _vector(self):
        """
        Plot course
        """
        vector_opt=(self._path1,self._path2,self._path3)     
        c = random.randint(0,(len(vector_opt)-1))
        return vector_opt[c]()
