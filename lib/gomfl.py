"""Example implementation.

Simple two mode structure, press the space bar to toggle and escape to quit.
Displays an additional label if DEBUG is enabled, try running run_game.py and
test_game.py.

"""

from __future__ import division

from pyglet import text
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode

import config
from common import *
from constants import *
import squirtle

from CrossHair import CrossHair

menu_label = text.Label("MENU", font_size=20)
game_label = text.Label("GAME", font_size=20)
debug_label = text.Label("DEBUG", font_size=20, y=24)


## Menu
#######

class MenuRenderer(mode.Renderer):

    def on_draw(self):
        self.handler.window.clear()
        menu_label.draw()
        spacebar = text.Label("Press Space to switch modes", font_size=30).draw
        if DEBUG:
            debug_label.draw()

class MenuMode(mode.Mode):
    name = "menu"
    renderer = MenuRenderer

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("game")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED
       

## Game
#######

class GameRenderer(mode.Renderer):        
    def on_draw(self):
        self.handler.window.clear()
        game_label.draw()
        self.handler.angle += 1
        self.handler.angle = self.handler.angle % 360
        if(self.handler.svg):    
		   self.handler.svg.draw(500, 400, angle=self.handler.angle, scale=1)

        if DEBUG:
            debug_label.draw()
            
        self.handler.crossHair.draw()

        
class GameMode(mode.Mode):
    name = "game"
    renderer = GameRenderer
    tick_count = 0
    svg = None
    angle = 0
    
    def __init__(self):
        mode.Mode.__init__(self)
        #self.svg = squirtle.SVG('sample.svg', anchor_x='center', anchor_y='center')
        #squirtle.setup_gl()
        #self.window.set_mouse_visible(False)
        self.crossHair = CrossHair()
        self.crossHair.handler = self

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        #print x,y,dx,dy
        self.crossHair.x = x
        self.crossHair.y = y

