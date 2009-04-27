"""Main starter module.

The DEBUG constant can be safely assumed set by the time this module is
imported.

"""

from __future__ import division

from pyglet import app
from pyglet import clock
from pyglet import window
from pyglet.gl import *

import data
import mode

import config
from common import *
from constants import *

import examples


class Controller(object):
    """Top level controller object.

    An instance of this represents an instance of the game. There is a brief
    chain of function calls, which ends with the `run` method here and then
    `pyglet.app.run`, which is the way the game is started.

    Modes and handlers are the abstraction of interface. A mode is a class and
    a handler is an instance of a mode. Modes are described in the `mode`
    module.

    """

    def __init__(self):
        self._handler = None
        self.suspended = {}

    def get_handler(self):
        return self._handler

    def set_handler(self, value):
        if self._handler is not None:
            self._handler.disconnect()
            self.window.pop_handlers()
            self._handler = None
        if value is not None:
            self._handler = value
            self.window.push_handlers(value)
            value.connect(self)

    handler = property(get_handler, set_handler)

    def switch_handler(self, name, *args, **kwds):
        """Connect a new handler.

        Additional arguments are passed to the mode constructer.

        :Parameters:
            `name` : str
                The name of the mode class to use.
            `suspend` : bool
                Default False. If True, the current mode is suspended rather
                than dropped.

        """
        suspend = kwds.pop("suspend", False)
        if suspend:
            self.suspend_handler()
        self.handler = mode.get_handler(name, *args, **kwds)

    def resume_handler(self, name, suspend=True):
        """Resume an old handler.

        Only one mode handler for each mode is stored. If another handler for
        the same mode is suspended then only the newer one can be resumed.

        :Parameters:
            `name` : str
                The name of the mode class to resume.
            `suspend` : bool
                Default False. If True, the current mode is suspended rather
                than dropped.

        """
        handler = self.suspended.pop(name)
        if suspend:
            self.suspend_handler()
        self.handler = handler
        self.handler = self.suspended.pop(mode)

    def clear_handler(self):
        """Clear the current handler, if any.

        """
        if self.handler is not None:
            self.handler = None

    def suspend_handler(self):
        """Suspend the current handler, if any.

        """
        if self.handler is not None:
            self.suspended[type(self.handler).name] = self.handler
            self.handler = None

    def tick(self, dt):
        """Update the game logic.

        """
        if self.handler is not None:
            self.handler.tick()

    def update(self, dt):
        """Maintain parallel features.

        :Parameters:
            `dt` : float
                The actual time since the last update was called.

        """
        if self.handler is not None:
            self.handler.update(dt)

    def setup_gl(self):
        """Configure GL properties.

        """
        self.window.switch_to()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        self.window.clear()
        self.window.flip()

    def setup_pyglet(self):
        """Configure Pyglet attributes.

        """
        self.window = window.Window(visible=False, caption=CAPTION,
                fullscreen=config.fullscreen)
        clock.schedule_interval_soft(self.tick, 1.0 / TICK_RATE)
        clock.schedule_interval_soft(self.update, 1.0 / UPDATE_RATE)

    def run(self):
        """Start the game.

        """
        self.setup_pyglet()
        self.setup_gl()
        self.switch_handler("menu")
        self.window.set_visible()
        app.run()


## Main function
################

def main():
    """Start the game.

    """
    if config.profile:
        import datetime, os, profile
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(SCRIPT_DIR, "profile-%s.log" % timestamp)
        profile.runctx("Controller().run()", globals(), None, filename)
    else:
        Controller().run()
