''' Menu '''

import os.path

import pyglet
from pyglet import text
from pyglet import image
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key
from pyglet.window import mouse

import mode
import config
from common import *
from constants import *

import degrees_of_awesome

menu_label = text.Label("MENU", font_size=20)

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
