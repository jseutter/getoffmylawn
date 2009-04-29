"""Example implementation.

Testing ground for graphics:
- pick a bad guy
- pick a starting place
- pick a path

"""

import random
import math

target_list = {"cross1":"crosshair.svg","cross2":"crosshair.svg"}

class GetTarget():
    name="GetTargets"

    def __init__(self):
        #one 60th of  sec
        self.name = "Target"
        
        # Look and feel
        self.left=None
        self.righ=None
        self.dead=None
        # The scaling size should be related to the y position
        self.scale=1
        
        # What path to take and path options
        self.attack_path=self._vector()
        
        # Speed and strenght options
        self.speed=1
        self.speed_multiply=1
        self.strength=1
        
        # screen position defaults and setup
        self.ymax=300
        self.ymin=275
        self.xmax=790
        self.xmin=10
        self.ystart = random.randint(self.ymin,self.ymax)
        self.xstart = random.randint(self.xmin,self.xmax)
        self.xloc=0
        self.yloc=0
    
        #Load a target
        self._load()
    
    def _load(self):
        """
        Load and pick a picture for this target
        """
        c = random.randint(0,(len(target_list.keys())-1))
        load_key = target_list.keys()[c]
                
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
        
    
        