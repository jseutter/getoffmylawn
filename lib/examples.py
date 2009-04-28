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
    svg = None
    angle = 0
    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        squirtle.setup_gl()
        self.svg = squirtle.SVG('sample.svg', anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.handler.window.clear()
        game_label.draw()
        self.angle += 1
        self.angle = self.angle % 360
        if(self.svg):
            self.svg.draw(500, 400, angle=self.angle, scale=1)

        if DEBUG:
            debug_label.draw()

class GameMode(mode.Mode):
    name = "game"
    renderer = GameRenderer
    tick_count = 0

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

