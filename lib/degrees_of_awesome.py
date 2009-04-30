import mode
import config
from pyglet.window import key
from constants import *
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
import pyglet

degrees = {
    1 : ('First Achievement', "Get this by being awesome"),
    2 : ('Second Achievement', "Get this by being awesome"),
    3 : ('Third Achievement', "Get this by being awesome"),
    4 : ('Fourth Achievement', "Get this by being awesome"),
    5 : ('Fifth Achievement', "Get this by being awesome"),
    6 : ('Sixth Achievement', "Get this by being awesome"),
    7 : ('Seveth Achievement', "Get this by being awesome"),
    8 : ('Eighth Achievement', "Get this by being awesome"),
    9 : ('Nineth Achievement', "Get this by being awesome"),
    10 : ('Tenth Achievement', "Get this by being awesome")
}

achievements = config.achievements

def unlock(degree):
    if (achievements[degree - 1] == 1):
        pass #already unlocked
    else:
        achievements[degree - 1] = 1
        config.save_option('achievements', achievements)

class AwesomeRenderer(mode.Renderer):
    bar = pyglet.image.load('resources/achievement_bar.png')
    amsterdam = None
    star = pyglet.image.load('resources/star.png')
    lock = pyglet.image.load('resources/lock.png')
    backdrop = pyglet.image.load('resources/non_gomfl_background.png')
    
    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        pyglet.font.add_file('resources/amsterdam.ttf')
        self.amsterdam = pyglet.font.load('Amsterdam Graffiti', 45)
        if(not self.handler.menu_boxes):
            self.handler.menu_boxes = []
            for i in range(10):
                self.handler.menu_boxes.append((50, 700, 
                    575 - i * BAR_HEIGHT, 575 - (i + 1) * BAR_HEIGHT))

    def _blit_bar(self, i):
        offset = 0
        if (i == self.handler.selected):
            offset = -30

        self.bar.blit(50 + offset, 520 - i * BAR_HEIGHT)

        if (self.handler.achievements[i] == 1):
            self.star.blit (60 + offset, 523 - i * BAR_HEIGHT)
        else:    
            self.lock.blit (60 + offset, 523 - i * BAR_HEIGHT)
            
        pyglet.font.Text(self.amsterdam, 
                         degrees[i+1][0], 
                         120 + offset, 
                         535 - i * BAR_HEIGHT, 
                         color=(0.27,0.125,0,1)).draw()

    def on_draw(self):
        self.handler.window.clear()

        self.backdrop.blit(0, 0)
        
        for i in range(10):
            self._blit_bar(i)

class AwesomeMode(mode.Mode):
    name = "awesome"
    renderer = AwesomeRenderer
    selected = 0
    menu_boxes = None
    achievements = config.achievements
    
    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            pass
        elif sym == key.DOWN:
            if self.selected < 9:
                self.selected += 1
        elif sym == key.UP:
            if self.selected > 0:
                self.selected -= 1
        elif key.ESCAPE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):   
        for (x_min, x_max, y_max, y_min), index in zip(self.menu_boxes, range(10)):
            if (x > x_min and
                x < x_max and
                y > y_min and
                y < y_max):
                self.selected = index

    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            pass        