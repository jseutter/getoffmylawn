'''
Gomfl Enemies
'''

from base import Character, create_svg
import degrees_of_awesome

class Ninja(Character):
    total_killed = 0
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.right = create_svg('ninja.svg')
        self.left = create_svg('ninja.svg')
        #self.dead = None 

    def hit(self, x, y):
        """
        Return 1 if the target is hit by a bullet at x,y
        """
        # target is anchord center, bottom
        width = self.right.width * self.scale
        height = self.right.height * self.scale
        
        # lower left hand coords
        lx = self.x - (width)/2.0
        ly = self.y
        
        # upper right hand coords
        tx = self.x + (width)/2.0
        ty = self.y + height
        
        if (x > lx and x < tx and
            y > ly and y < ty):
            Ninja.total_killed += 1
            if (Ninja.total_killed == 100):
                degrees_of_awesome.unlock(2)
            return 1
        return 0
        

# A list of enemies
ENEMIES = [Ninja, ]
