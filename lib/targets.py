"""Example implementation.

Testing ground for graphics:
- pick a bad guy
- pick a starting place
- pick a path

"""

import random
import characters
from constants import *

def get_random_target_class(targets=characters.enemies.ENEMIES):
    return targets[int(random.random() * len(targets))]

def get_random_target(targets=characters.enemies.ENEMIES):
    return get_random_target_class(targets)()

class TargetController(object):
    ''' Class to handle difficulty associated with targets '''

    EASY='sissy'
    MEDIUM='normal'
    HARD='ouch'
    MULT_T = 10  # use multiplier every `MULT_T` secs

    def __init__(self, difficulty='sissy'):
        self.targets = []
        self.hit=0
        self.difficulty = difficulty
        if self.difficulty == self.EASY:
            self.speed = 0.1
            self.strength = 1
            self.speed_multiply = 0.01
            self.release_rate = 3 # ticks
            self.relive_count = 3
        elif self.difficulty == self.MEDIUM:
            self.speed = 0.3
            self.strength = 2
            self.speed_multiply = 0.05
            self.release_rate = 2 # ticks
            self.relive_count = 5
        else: #if self.difficulty == self.HARD:
            self.speed = 0.7
            self.strength = 3
            self.speed_multiply = 0.1
            self.release_rate = 1 # ticks
            self.relive_count = 7
        if DEBUG:
            print 'Difficulty set to: %s' %(self.difficulty)

    def generate_target(self, t):
        ''' Generates a target.
        `t` (time from start) is used to update game speed
        Generated targets are stored in `self.targets`
        '''
        multiplier = 1 + self.speed_multiply * (int(t/self.MULT_T)+1)
        t = get_random_target_class()(speed=self.speed*multiplier)
        self.targets.append(t)
        if DEBUG:
            print 'Target Created with Speed: %.2f Using Mult: %.2f' %(
                    self.speed*multiplier, multiplier)

        