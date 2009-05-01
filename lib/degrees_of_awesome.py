import mode
import config
from pyglet.window import key
from constants import *
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import mouse
from pyglet import image
from pyglet import font
from pyglet.media import StaticSource
from pyglet.media import load

degrees = {
    1 : ('Starting Out', "Got the Game Running"),
    2 : ('Killah', "Killed 100 Ninjas"),
    3 : ('Lazy Eye', "5 Hits in a Row, without a single miss"),
    4 : ('Dead Eye', "100 Hits in a Row, without a single miss"),
    5 : ('Mechanic', "Killed 100 Robots"),
    6 : ('Ah-Gee', "Earn 1,000 points"),
    7 : ('10k', "Earn 10,000 points"),
    8 : ('Also Ran', "At 100 kills have an accuracy of at least 85%"),
    9 : ('Biased', "Kill 5 Robots in a row without killing a single Ninja"),
    10 : ('Open Source', "Modified local.py to give yourself all the achievement, cuz you know you are like that")
}

achievements = config.achievements
new_achievements = []
achievement_sound =  StaticSource(load('resources/sounds/drop.ogg'))
def unlock(degree):
    if (achievements[degree - 1] == 1):
        pass #already unlocked
    else:
        achievement_sound.play()
        achievements[degree - 1] = 1
        config.save_option('achievements', achievements)
        new_achievements.append(degrees[degree])

class AwesomeRenderer(mode.Renderer):
    bar = image.load('resources/achievement_bar.png')
    amsterdam = None
    amsterdam_detail = None
    star = image.load('resources/star.png')
    lock = image.load('resources/lock.png')
    backdrop = image.load('resources/non_gomfl_background.png')
    dialog = image.load('resources/achievement_dialog.png')
    
    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        font.add_file('resources/amsterdam.ttf')
        self.amsterdam = font.load('Amsterdam Graffiti', 45)
        self.amsterdam_detail = font.load('Amsterdam Graffiti', 24)
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
            self.star.blit (60 + offset, 519 - i * BAR_HEIGHT)
        else:    
            self.lock.blit (60 + offset, 523 - i * BAR_HEIGHT)
            
        font.Text(self.amsterdam, 
                         degrees[i+1][0], 
                         120 + offset, 
                         535 - i * BAR_HEIGHT, 
                         color=(0.27,0.125,0,1)).draw()

    def on_draw(self):
        self.handler.window.clear()

        self.backdrop.blit(0, 0)
        
        for i in range(10):
            self._blit_bar(i)
            
        if (not self.handler.displayed_degree is None):
            self.dialog.blit(0, 0)
            font.Text(self.amsterdam,
                      degrees[self.handler.displayed_degree + 1][0],
                      250,
                      400,
                      width=300,
                      color=(0.27,0.125,0,1)).draw()
            font.Text(self.amsterdam_detail,
                    #degrees[self.handler.displayed_degree + 1][0],
                    degrees[self.handler.displayed_degree + 1][1],
                    225,
                    350,
                    width=350,
                    color=(0.27,0.125,0,1)).draw()
                      

            

class AwesomeMode(mode.Mode):
    name = "awesome"
    renderer = AwesomeRenderer
    selected = 0
    menu_boxes = None
    achievements = config.achievements
    displayed_degree = None
    
    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            if(self.displayed_degree):
                self.displayed_degree = None
            else:
                self.displayed_degree = self.selected
        elif sym == key.DOWN:
            if self.selected < 9:
                self.selected += 1
        elif sym == key.UP:
            if self.selected > 0:
                self.selected -= 1
        elif key.ESCAPE:
            if(self.displayed_degree):
                self.displayed_degree = None
            else:
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
            if(self.displayed_degree):
                self.displayed_degree = None
            else:
                self.displayed_degree = self.selected