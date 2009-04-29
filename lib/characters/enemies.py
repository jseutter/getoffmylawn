'''
Gomfl Enemies
'''

from base import Character

class Bunny(Character):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

# A list of enemies
ENEMIES = [Bunny, ]
