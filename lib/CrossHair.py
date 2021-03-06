from pyglet import window
from pyglet import clock
from pyglet import font
import random

import os

from pyglet import image
import squirtle

class CrossHair:
    def __init__(self, *args, **kwargs):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.handler = None
        self.svg = squirtle.SVG('resources/crosshair.svg', anchor_x='center', anchor_y='center')
        
    def draw(self):
        self.svg.draw(self.x, self.y, z=1, angle=self.angle, scale=0.1)
        self.angle = (self.angle + 1) % 360
