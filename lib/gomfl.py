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
from pyglet.window import mouse

import pyglet
import mode

import config
from common import *
from constants import *
import squirtle
import degrees_of_awesome

from CrossHair import CrossHair

# targets is the target class
import targets
import time

menu_label = text.Label("MENU", font_size=20)
game_label = text.Label("GAME", font_size=20)
debug_label = text.Label("DEBUG", font_size=20, y=24)

GOMFL_HEIGHT = 281
MENU_IMAGE_HEIGHT = 80
MENU_IMAGE_MARGIN = 70

## Menu
#######

class MenuRenderer(mode.Renderer):
    up_images = []
    down_images = []
    menu_names = ['play', 'highscores', 'degrees', 'quit']

    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        for menu_item in self.menu_names:
            self.up_images.append(pyglet.image.load('resources/menu_images/' + menu_item + "_up.png"))
            self.down_images.append(pyglet.image.load('resources/menu_images/' + menu_item + "_down.png"))

    def on_draw(self):
        self.handler.window.clear()
        backdrop = pyglet.image.load('resources/gomfl_background.png')
        backdrop.blit(0, 0)
        for i in range(4):
            if self.handler.selected == i:
                self.down_images[i].blit(MENU_IMAGE_MARGIN, GOMFL_HEIGHT - MENU_IMAGE_HEIGHT * i)
            else:
                self.up_images[i].blit(MENU_IMAGE_MARGIN, GOMFL_HEIGHT - MENU_IMAGE_HEIGHT * i)
                

class MenuMode(mode.Mode):
    """
    0 = play
    1 = high scores
    2 = degrees
    3 = quit
    """
    name = "menu"
    renderer = MenuRenderer
    selected = 0
    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            if self.selected == 0:
                self.control.switch_handler("game")
            elif self.selected == 2:
                self.control.switch_handler("awesome")
            elif self.selected == 3:
                pyglet.app.exit()
        elif sym == key.DOWN:
            if self.selected < 3:
                self.selected += 1
        elif sym == key.UP:
            if self.selected > 0:
                self.selected -= 1
        elif key.ESCAPE:
            pyglet.app.exit()
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
        
        #Move existing targets if any
        #for t in self.target_list:
        #    t.draw()
        
        
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
        self.target_list=[]
        self.runtime=time.time()
        
    def update(self,dt):

        #for t in self.target_list:
            #print "Moving target"
            #Move current targets
            #t.move()
            
        # Create new targets when needed
        
        # If we kill all targets then create a bunch right away
        if (len(self.target_list) < 1):
            for i in range(1,5):
                t = targets.GetTarget()
                self.target_list.append(t)
        
        print "Rate: %s"%(dt)
        
        
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
        
    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            print "Pressed left mouse button"
        # Check targets
        # For t in target_list:
        #   if t.hit(x,y):
        #     t.death
        #     ....

