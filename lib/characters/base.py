'''
Base class for characters
'''

import os.path
import math
import random
from .squirtle import SVG
from .constants import DEBUG 

ANGLES=[x for x in range(5,-1,-1)] + [x for x in range(359,349,-1)] + [x for x in range(351,360)] + [x for x in range(0,5)]

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
    SCALEMAX = 1.7
    SCALEMIN = 0.03
    ZMAX = 300
    ZMIN = 0
    ZBUFFER = 50 # allow things to go this much off screen (Z-Axis)

    # Look and feel
    LEFT = 'left'
    RIGHT = 'right'
    DEAD = 'dead'
    left=None
    right=None
    dead=None
    time_til_switch = 0

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
        self.angle = 0 #random.randint(0, len(ANGLES)-1)
        self.curr_view = self.LEFT
        self.speed = speed
        self.strength = strength
        self.name = self.__class__.__name__
        self.is_dead = 0
        self.deadtime = 0

    def _update_vector(self):
        '''
        updates the motion vector

        `self.v.x` is updated based on `self.x` location
        There exists conditions to ensure character is within X-axis limits.
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
        if (not self.curr_view == self.DEAD):
            dt *= 100 # time increment is normally quite small
            self._update_vector()
            if self.z > self.ZMIN - self.ZBUFFER:
                self.z += dt * self.v.z * self.speed
            self.y = self.z
            self.x += dt * self.v.x * self.speed
            self.angle = 0 #(self.angle + 1) % len(ANGLES)
            self.scale = (
                    (self.SCALEMAX - self.SCALEMIN) / (self.ZMAX - self.ZMIN)
                ) * (self.ZMAX - self.z) + self.SCALEMIN
            if not self.is_dead:
                if self.time_til_switch <= 0:
                    self.curr_view = self.RIGHT \
                        if self.curr_view == self.LEFT else self.LEFT
                    self.time_til_switch = 10
                self.time_til_switch -= dt

    def draw(self):
        getattr(self, self.curr_view).draw(self.x, self.y, angle=self.angle, scale=self.scale)

    def sepuku(self):
        """ we must now die honorably like a true samurai"""
        self.is_dead = 1
        self.curr_view = self.DEAD
