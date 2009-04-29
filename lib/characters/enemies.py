'''
Gomfl Enemies
'''

from base import Character, create_svg

class Bunny(Character):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.right = create_svg('ninja.svg')
        self.left = create_svg('ninja.svg')
#         self.dead = None 

# A list of enemies
ENEMIES = [Bunny, ]
