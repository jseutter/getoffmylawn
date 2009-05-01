'''
Gomfl Enemies
'''

from base import Character, create_svg
import degrees_of_awesome
from pyglet import clock

class Ninja(Character):
    total_killed = 0

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.right = create_svg('ninja_right.svg')
        self.left = create_svg('ninja.svg')
        self.dead = create_svg('ninja_death.svg')

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
            Robot.in_a_row = 0
            if (Ninja.total_killed == 100):
                degrees_of_awesome.unlock(2)
            return 1
        return 0


# A list of enemies
class Robot(Character):
    total_killed = 0
    in_a_row = 0

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.right = create_svg('robot_right.svg')
        self.left = create_svg('robot_left.svg')
        self.dead = create_svg('robot_death.svg')

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
            Robot.total_killed += 1
            Robot.in_a_row += 1
            if (Robot.total_killed == 100):
                degrees_of_awesome.unlock(5)
            if (Robot.in_a_row == 5):
                degrees_of_awesome.unlock(9)
            return 1
        return 0

ENEMIES = [Ninja,Robot ]
