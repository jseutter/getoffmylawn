''' Game '''

from __future__ import division

import os.path

from pyglet import text
from pyglet import font
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key
from pyglet.window import mouse

import mode
import squirtle
import config
import degrees_of_awesome

from common import *
from constants import *

from CrossHair import CrossHair

# targets is the target class
import targets
import time

game_label = text.Label("GAME", font_size=20)
debug_label = text.Label("DEBUG", font_size=20, y=24)

MAX_TARGETS = 100

class GameRenderer(mode.Renderer):
    amsterdam = None

    def __init__(self, handler):
         mode.Renderer.__init__(self, handler)
         font.add_file('resources/amsterdam.ttf')
         self.amsterdam = font.load('Amsterdam Graffiti', 24)
    
    def on_draw(self):
        self.handler.window.clear()

        self.handler.background.draw(0,0,z=0.5)
        self.handler.crossHair.draw()
        #game_label.draw()

        hits = text.Label("Hits:  %s"%(self.handler.hits),font_size=20,x=700,y=570)
        miss = text.Label("Miss: %s"%(self.handler.miss),font_size=20,x=700,y=545)
        
        hits.draw()
        miss.draw()
        
        if DEBUG:
            debug_label.draw()

        self.handler.crossHair.draw()

        #Move existing targets if any
        for t in self.handler.target_list:
            t.draw()

        # Show achievement unlocked
        if (self.handler.achievement_counter):
            self.handler.achievement_counter -= 1
            self._blit_degree_unlocked("You Rock, Your Degree of Awesomeness has increased")
        elif (degrees_of_awesome.new_achievements):
            degree_text = degrees_of_awesome.new_achievements.pop()
            self._blit_degree_unlocked("You Rock, Your Degree of Awesomeness has increased")
            self.handler.achievement_counter = 100

    def _blit_degree_unlocked(self, text):
        font.Text(self.amsterdam, 
                     text, 
                     100, 
                     300, 
                     color=(0.9,0.1,0.1,1)).draw()

class GameMode(mode.Mode):
    name = "game"
    renderer = GameRenderer
    tick_count = 0
    background = None
    angle = 0
    achievement_counter = None
    def __init__(self):
        mode.Mode.__init__(self)
        squirtle.setup_gl()

        self.background = squirtle.SVG("resources/backdrop.svg")

        self.crossHair = CrossHair()
        self.crossHair.handler = self
        self.target_list=[]
        self.runtime=time.time()
        self.timestamp=0
        self.hits=0
        self.miss=0

    def update(self,dt):

        for t in self.target_list:
            #print "Moving target"
            #Move current targets
            oldx = t.x
            t.move()
            if oldx < t.x:
                t.current_view = t.LEFT
            elif oldx > t.x:
                t.curr_view = t.RIGHT
            else: # no x motion, just swap the view
                t.curr_view = t.RIGHT if t.curr_view == t.LEFT else t.LEFT
            t.current_view = t.LEFT

        # Create new targets when needed
        self.timestamp+=dt
        run_len=time.time() - self.runtime
        mult = run_len % 3.0

        #if DEBUG:
        #    print "Rate: %s   Multi: %s"%(self.timestamp,mult)

        create_target = False
        if (self.timestamp > 0.5):
            self.timestamp=0
            create_target = True
        if (0 == mult):
            create_target = True

        if create_target:
            count = 1
            if (len(self.target_list) < 1):
                # If we kill all targets then create a bunch right away
                count = 3
            
            for i in range(count):
                if (len(self.target_list) < MAX_TARGETS):
                    t = targets.get_random_target()
                    self.target_list.append(t)

            if DEBUG:
                print "Creating target"

            if (len(self.target_list) == 5):
                print "fired"
                degrees_of_awesome.unlock(1)


    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        #print x,y,dx,dy
        self.window.set_mouse_visible(False)
        self.crossHair.x = x
        self.crossHair.y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)

    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            print "Pressed left mouse button (%s, %s)" %(x,y)
            
        # Check targets
        check_hit=0
        for t in self.target_list:
            if t.hit(x,y):
                self.target_list.remove(t)
                check_hit=1
                break
          
        if 1 == check_hit:
            self.hits +=1
        else:
            self.miss +=1
             

