''' Game '''

from __future__ import division

import os.path

from pyglet import text
from pyglet import font
from pyglet import image
from pyglet import clock
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
import random

from pyglet.media import StaticSource
from pyglet.media import load

game_label = text.Label("GAME", font_size=20)
debug_label = text.Label("DEBUG", font_size=20, y=24)

MAX_TARGETS = 100

class GameRenderer(mode.Renderer):
    amsterdam = None
    degree_text = None
    achievement_popup = squirtle.SVG("resources/achievement_popup.svg")

    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        font.add_file('resources/amsterdam.ttf')
        self.amsterdam = font.load('Amsterdam Graffiti', 45)

    def on_draw(self):

        if self.handler.pause:
            self._blit_text('     Pause', '')
            return

        self.handler.window.clear()
        self.handler.background.draw(0,0,z=0.5)

        # Stats Calc
        health = (self.handler.HEALTH -
                    self.handler.health_loss) / self.handler.HEALTH
        try:
            accuracy_value = self.handler.hits / (self.handler.hits + self.handler.miss)
        except ZeroDivisionError:
            accuracy_value = 1.0
        accuracy_color = (int((1 - accuracy_value) * 255), int(accuracy_value * 255), 0, 255)

        if(self.handler.hits == 100 and accuracy_value > 0.85):
            degrees_of_awesome.unlock(8)

        # TODO: Put some monospace font here
        labels = []
        label_properties = dict(font_size=20, color=accuracy_color, anchor_x='right', halign='right')
        y = 595
        for l,v in [
            ('Hits', str(self.handler.hits)),
            ('Miss', str(self.handler.miss)),
            ('Acc', '%.0f%%' %(accuracy_value*100)),
            ('Score', str(self.handler.score)),
            ('Health', '%.0f%%' %(health*100))]:
            y -= 25
            labels.append(text.Label(l, x=795, y=y, **label_properties))
            labels.append(text.Label(v, x=700, y=y, **label_properties))

        for l in labels:
            l.draw()

        # Show some text that stating well done
        if self.handler.game_complete:
            text.Label(
                'GAME COMPLETED',
                font_name='Times New Roman',
                font_size=36,
                color=(64,64,64,128),
                x=self.handler.window.width//2,
                y=self.handler.window.height-50,
                anchor_x='center',
                anchor_y='center').draw()

        if DEBUG:
            debug_label.draw()

        self.handler.crossHair.draw()

        # Redraw existing targets
        for t in reversed(self.handler.target_controller.targets):
            t.draw()

        # Health Bar
        self.handler.health_bar.draw(25,10,scale=(health,1))

        # The game is over, but let the poor guy play neways
        if self.handler.game_over:
            self._blit_text('who cares?', 'Game Over, but')

        # Show some text at the end of the level
        if self.handler.level_anime == 1:
            self._blit_text('  Complete', 'Level %s' %(
                self.handler.target_controller.level))
        elif self.handler.level_anime == 2:
            self._blit_text('    Level %s' %(
                self.handler.target_controller.level+1), 'Proceed...')
        elif self.handler.level_anime == 3:
            self._blit_text('', '    - HAI -')

        # Show achievement unlocked
        if (self.handler.achievement_counter):
            self.handler.achievement_counter -= 1
            self._blit_text(self.degree_text)
        elif (degrees_of_awesome.new_achievements):
            self.degree_text = degrees_of_awesome.new_achievements.pop()[0]
            self._blit_text(self.degree_text)
            self.handler.achievement_counter = 75

    def _blit_text(self, text, header='Unlocked:'):
        ''' Blit Text on Screen, Mainly for displaying unlocked degrees '''
        self.achievement_popup.draw(500, 50)
        font.Text(
            self.amsterdam, header, 525, 120,
            color=(0.27,0.125,0,1)).draw()
        font.Text(
            self.amsterdam, text, 525, 75,
            color=(0.27,0.125,0,1)).draw()

class GameMode(mode.Mode):
    name = "game"
    pause = False
    renderer = GameRenderer
    tick_count = 0
    background = None
    angle = 0
    achievement_counter = None
    in_a_row = 0
    gunshot = StaticSource(load('resources/sounds/gunshot.ogg'))
    hlaugh = StaticSource(load('resources/sounds/horrible_laugh.ogg'))
    ninja_death=[StaticSource(load('resources/sounds/ninja_death_1.ogg')),StaticSource(load('resources/sounds/ninja_death_2.ogg')),StaticSource(load('resources/sounds/ninja_death_3.ogg'))]
    SDDOWN = 10 # inverse prop to score
    HDDOWN = 10 # inverse prop to health *loss*
    LAWN_ZMAX = 280
    HEALTH = 1000000
    LEVELS = [1000, 3000, 5000, 10000]
    game_complete = False
    level_anime = 0

    def __init__(self):
        mode.Mode.__init__(self)
        squirtle.setup_gl()

        self.background = squirtle.SVG("resources/backdrop.svg")
        self.health_bar = squirtle.SVG("resources/health_bar.svg")

        self.crossHair = CrossHair()
        self.crossHair.handler = self
        self.target_controller = TargetController(TargetController.MEDIUM)
        self._update_difficulty(TargetController.MEDIUM)
        self.runtime=time.time()
        self.timestamp=0
        self.hits=0
        self.miss=0
        self.score=0
        self.health_loss = 0

        GameMode.hlaugh.play()

    def _update_difficulty(self, difficulty):
        ''' update vars related to `difficulty` '''
        if difficulty == TargetController.EASY:
            self.SDDOWN = 20
            self.HDDOWN = 3
        elif difficulty == TargetController.MEDIUM:
            self.SDDOWN = 15
            self.HDDOWN = 2
        else: # difficulty == TargetController.HARD:
            self.SDDOWN = 10
            self.HDDOWN = 1

    def _is_game_over(self):
        if self.health_loss >= self.HEALTH:
            self.health_loss = self.HEALTH
            return True
        return False
    game_over = property(_is_game_over)

    def killall(self):
        ''' kill all targets '''
        for t in self.target_controller.targets:
            t.sepuku()

    @staticmethod
    def _level_anime(dt, self):
        if self.level_anime <= 3:
            self.level_anime += 1
            clock.schedule_once(self._level_anime, 2, self)
        else:
            self.level_anime = -1
        if DEBUG:
            print 'LEVEL END ANIMATION (%s)' %(self.level_anime)

    def update(self,dt):
        ''' Update game state '''
        if self.pause or self.level_anime > 0:
            return
        elif self.level_anime == -1:
            if self.target_controller.level + 1 > len(self.LEVELS):
                self.game_complete = True
            self.target_controller = TargetController(
                self.target_controller.difficulty,
                self.target_controller.level + 1)
            self.level_anime = 0
        elif not (self.game_complete or self.level_anime) and (
            self.score > self.LEVELS[self.target_controller.level - 1]):
            self.level_anime = 1
            clock.schedule_once(self._level_anime, 2.5, self)
            self.killall()

        for t in self.target_controller.targets:
            if (not t.is_dead):
                # Calculate the health kill
                if t.z < self.LAWN_ZMAX:
                    self.health_loss += (self.LAWN_ZMAX - t.z) / self.HDDOWN
                # Move Target
                t.move(dt)
            else:
                # they killed Kenny!
                t.deadtime+=dt
                if (t.deadtime > self.target_controller.max_deadtime):
                    self.target_controller.targets.remove(t)

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
            if (not len(filter(
                    lambda t: not t.is_dead,
                    self.target_controller.targets))):
                # If we clear all targets then create a bunch right away
                count = self.target_controller.relive_count
            for i in range(count):
                if (len(self.target_controller.targets) < MAX_TARGETS):
                        self.target_controller.generate_target(run_len)

    def on_key_press(self, sym, mods):
        if DEBUG:
            print 'KeyPress:', sym, 'Mods:', mods
        if sym == key.SPACE:
            # self.control.switch_handler("menu")
            self.pause = False if self.pause else True
        elif mods & key.MOD_CTRL and mods & key.MOD_SHIFT:
            # Cheats
            if sym == key.A:
                self.killall()
            elif sym == key.S:
                self.score += 500
            elif sym == key.W:
                self.target_controller.speed_down()
            elif sym == key.E:
                self.target_controller.speed_up()
            elif sym == key.R:
                self.target_controller.speed_restore()
            elif sym == key.Q:
                self.HEALTH = self.health_loss + 100000
            elif sym == key.D:
                self.game_complete = True
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
            GameMode.gunshot.play()
            if DEBUG:
                print "Pressed left mouse button (%s, %s)" %(x,y)

            # Check targets for hit
            check_hit=0
            for t in self.target_controller.targets:
                if not t.is_dead and t.hit(x,y):
                    c = random.randrange(0,3)
                    GameMode.ninja_death[c].play()
                    t.sepuku()
                    check_hit=1
                    if DEBUG:
                        print t.id, '(%.f, %.f, %.f)'%(t.x, t.y, t.z), 'killed'
                    break

            # Score and Awesomeness degree
            if check_hit:
                self.hits +=1
                self.in_a_row += 1
                # z-axis is the ground plane
                # score based on target position rather than mouse pos
                hit_score = int(t.z/self.SDDOWN)
                # Sometimes the target is past 0 (i.e. t.z is -ve)
                if hit_score > 0:
                    self.score += hit_score
                if(self.score >= 1000):
                    degrees_of_awesome.unlock(6)
                if(self.in_a_row == 5):
                    degrees_of_awesome.unlock(3)
                if(self.in_a_row == 100):
                    degrees_of_awesome.unlock(4)
            else:
                self.in_a_row = 0
                self.miss +=1
