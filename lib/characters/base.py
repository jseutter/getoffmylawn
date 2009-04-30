'''
Base class for characters
'''

import os.path
import math
import random
from .squirtle import SVG

ANGLES=[x for x in range(5,-1,-1)] + [x for x in range(359,349,-1)] + [x for x in range(351,360)] + [x for x in range(0,5)]
LEN_ANGLES=len(ANGLES)

def randomize_number(n):
    ''' A function to mess with a number '''
    return n * [1,-1][random.randint(0,1)]

def create_svg(file_name, anchor_x='center', anchor_y='bottom'):
    return SVG(
        os.path.join('resources', file_name),
        anchor_x=anchor_x,
        anchor_y=anchor_y)


class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z


class Character(object):
    ''' A generic GOMFL character '''

    # screen position defaults and setup
    SCALEMAX = 1.3
    SCALEMIN = 0.03
    ZMAX = 300
    ZMIN = 0

    # Look and feel
    LEFT = 'left'
    RIGHT = 'right'
    DEAD = 'dead'
    left=None
    right=None
    dead=None

    def __init__(self, speed=0.01, strength=1):
        '''
        Initializes a character at a given time `t`
        '''
        ymax, ymin = 300, 275
        xmax, xmin = 775, 50
        self.scale=self.SCALEMIN
        self.x = random.randint(xmin, xmax)
        self.y = random.randint(ymin, ymax)
        self.z = self.ZMAX
        self.v = Vector(0,0,-1) # initial motion vector
        self.v.x = [-4, 4][random.randint(0,1)]
        self.angle = random.randint(0, LEN_ANGLES-1)
        self.curr_view = self.LEFT
        self.speed = speed
        self.strength = strength
        self.name = self.__class__.__name__

    def _update_vector(self):
        '''
        updates the motion vector

        `self.v.x` is updated based on `self.x` location
        Two main conditions ensure the character to stays in screen.
        '''
        if self.x < 75: # Near the border
            self.v.x = 4
        elif 145 < self.x < 150:
            if random.randint(0,1):
                self.v.x = randomize_number(3)
        elif 220 < self.x < 225:
            if random.randint(0,1):
                self.v.x = randomize_number(2)
        elif 295 < self.x < 300:
            if random.randint(0,1):
                self.v.x = randomize_number(1)
        elif self.x > 725: # Near the border
            self.v.x = -4
        elif 650 < self.x < 655:
            if random.randint(0,1):
                self.v.x = randomize_number(-3)
        elif 575 < self.x < 580:
            if random.randint(0,1):
                self.v.x = randomize_number(-2)
        elif 500 < self.x < 505:
            if random.randint(0,1):
                self.v.x = randomize_number(-1)

    def move(self, dt):
        ''' updates location based on time elapsed `t` '''
        dt *= 100 # time increment is normally quite small
        self._update_vector()
        self.z += dt * self.v.z * self.speed
        self.y = self.z
        self.x += dt * self.v.x
        self.angle = (self.angle + 1) % LEN_ANGLES
        self.scale = (
                (self.SCALEMAX - self.SCALEMIN) / (self.ZMAX - self.ZMIN)
            ) * (self.ZMAX - self.z) + self.SCALEMIN

    def draw(self):
        getattr(self, self.curr_view).draw(self.x, self.y, angle=ANGLES[self.angle], scale=self.scale)
