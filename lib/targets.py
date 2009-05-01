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
    LEVEL_DIFF = 0.15 # % difficulty increase per level (0.15=15%)

    def __init__(self, difficulty='sissy', level=1):
        self.targets = []
        self.hit=0
        self.difficulty = difficulty
        self.level = level
        if self.difficulty == self.EASY:
            self.speed = 0.1
            self.strength = 1
            self.base_multiply = 0.01
            self.base_relive_count = self.relive_count = 3
            self.base_release_int = self.release_int = 3
        elif self.difficulty == self.MEDIUM:
            self.speed = 0.3
            self.strength = 2
            self.base_multiply = 0.05
            self.base_relive_count = self.relive_count = 5
            self.base_release_int = self.release_int = 2
        else: #if self.difficulty == self.HARD:
            self.speed = 0.7
            self.strength = 3
            self.base_multiply = 0.1
            self.base_relive_count = self.relive_count = 7
            self.base_release_int = self.release_int = 1
        if DEBUG:
            print 'Difficulty set to:', self.difficulty
            print 'Level:', self.level

    def get_multiplier(self, t):
        '''
        Calculates the multiplier for the current point in time `t`
        since the start of the game
        '''
        return (
            (1 + (self.level - 1) * self.LEVEL_DIFF) +
            self.base_multiply * (int(t/self.MULT_T)+1)
        )

    def update_variables(self, multiplier):
        ''' Updates variables by multiplier
        Call this to update TargetController game speed!
        '''
        self.relive_count = int(self.base_relive_count*multiplier)
        self.release_int = self.base_release_int / multiplier

    def generate_target(self, t):
        ''' Generates a target.
        `t` (time from start) is used to update game speed
        Generated targets are stored in `self.targets`
        '''
        multiplier = self.get_multiplier(t)
        self.update_variables(multiplier)
        t = get_random_target_class()(speed=self.speed*multiplier)
        self.targets.append(t)
        if DEBUG:
            print 'Target Created with Mult:', \
                    '%.2f Speed: %.2f, Release: %.2f,  Relive: %s'%(
                        multiplier, self.speed*multiplier, self.release_int,
                        self.relive_count)
