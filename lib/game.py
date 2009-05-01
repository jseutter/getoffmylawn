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
from targets import TargetController
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

        # Stats Calc
        try:
            accuracy_value = self.handler.hits / (self.handler.hits + self.handler.miss)
        except ZeroDivisionError:
            accuracy_value = 1.0
        accuracy_color = (int((1 - accuracy_value) * 255), int(accuracy_value * 255), 0, 255)

        # TODO: Put some monospace font here
        labels = []
        label_properties = dict(font_size=20, color=accuracy_color, anchor_x='right', halign='right')
        y = 595
        for l,v in [
            ('Hits', str(self.handler.hits)),
            ('Miss', str(self.handler.miss)), 
            ('Acc', '%.0f%%' %(accuracy_value*100)), 
            ('Score', str(self.handler.score))]:
            y -= 25
            labels.append(text.Label(l, x=795, y=y, **label_properties))
            labels.append(text.Label(v, x=700, y=y, **label_properties))
            # Trying to use the glyphs, to uncomment these you must mess with label_prop
            # labels.append(font.Text(self.amsterdam, l, x=795, y=y, **label_properties))
            # labels.append(font.Text(self.amsterdam, v, x=750, y=y, **label_properties))

        for l in labels: 
            l.draw()

        if DEBUG:
            debug_label.draw()

        self.handler.crossHair.draw()

        # Redraw existing targets
        for t in reversed(self.handler.target_controller.targets):
            t.draw()

        # Show achievement unlocked
        if (self.handler.achievement_counter):
            self.handler.achievement_counter -= 1
            self._blit_degree_unlocked("You Rock, Your Degree of Awesomeness has increased")
        elif (degrees_of_awesome.new_achievements):
            degree_text = degrees_of_awesome.new_achievements.pop()
            self._blit_degree_unlocked("You Rock, Your Degree of Awesomeness has increased")
            self.handler.achievement_counter = 200

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
    in_a_row = 0
    
    def __init__(self):
        mode.Mode.__init__(self)
        squirtle.setup_gl()

        self.background = squirtle.SVG("resources/backdrop.svg")

        self.crossHair = CrossHair()
        self.crossHair.handler = self
        self.target_controller = TargetController(TargetController.MEDIUM)
        self.runtime=time.time()
        self.timestamp=0
        self.hits=0
        self.miss=0
        self.score=0

    def update(self,dt):

        # Moving Targets
        for t in self.target_controller.targets:
            oldx = t.x
            t.move(dt)

        # Incrementing counters and timers
        self.timestamp+=dt
        run_len=time.time() - self.runtime

        # checking: should we create target(s)
        create_target = False
        if (self.timestamp > self.target_controller.release_int):
            self.timestamp=0
            create_target = True
        if create_target:
            # K Were supposed to create target(s)
            count = 1
            if (len(self.target_controller.targets) < 1):
                # If we kill all targets then create a bunch right away
                count = self.target_controller.relive_count

            for i in range(count):
                if (len(self.target_controller.targets) < MAX_TARGETS):
                    self.target_controller.generate_target(run_len)

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
            if DEBUG:
                print "Pressed left mouse button (%s, %s)" %(x,y)

            # Check targets for hit
            check_hit=0
            for t in self.target_controller.targets:
                if t.hit(x,y):
                    self.target_controller.targets.remove(t)
                    check_hit=1
                    if DEBUG:
                        print t.name, '(%.f, %.f)'%(t.x, t.y), 'killed. Success!'
                    break

            if 1 == check_hit:
                self.hits +=1
                self.in_a_row += 1
                self.score +=int(y/10)
                
                if(self.in_a_row == 5):
                    degrees_of_awesome.unlock(3)
                if(self.in_a_row == 100):
                    degrees_of_awesome.unlock(4)
            else:
                self.in_a_row = 0
                self.miss +=1
