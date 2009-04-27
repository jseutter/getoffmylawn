"""Interface object framework.

"""

from __future__ import division

from pyglet.window import key

import config
from common import *
from constants import *


#: Global directory of modes, updated automatically when modes are created.
mode_directory = {}

def get_handler(name, *args, **kwds):
    """Return a handler for the given mode name or None.

    Additional arguments are passed to the mode constructer.

    :Parameters:
        `name` : str
            The mode name to look for.

    """
    mode = mode_directory.get(name)
    if mode is not None:
        return mode(*args, **kwds)


class Renderer(object):
    """Base class for view objects.

    The purpose of a renderer is partly to take the responsibility for drawing
    things away from the mode, making the mode a pure interface and the renderer
    a pure view. It also allows us to make how to render a much more modular
    idea than if the rendering was done by the mode.

    """

    def __init__(self, handler):
        """Construct a Renderer object.

        :Parameters:
            `handler` : Mode
                The associated interface object.

        """
        self.handler = handler

    def on_draw(self):
        """Render the handler.

        """
        self.handler.window.clear()


class ModeMeta(type):
    """Metaclass for interface objects.

    Updates the mode directory when a new mode is created.

    """

    def __init__(self, *args, **kwds):
        """Construct a ModeMeta object.

        """
        super(ModeMeta, self).__init__(*args, **kwds)
        if self.name is None and None in mode_directory:
            raise AssertionError, "must override mode name in subclasses"
        elif self.name in mode_directory:
            raise AssertionError, "mode %r already exists" % self.name
        mode_directory[self.name] = self


class Mode(object):
    """Base class for interface objects.

    Modes have an update method that is called every tick and define event
    handlers for the window and controller. Handlers (instances of a mode) are
    automatically pushed onto the window and controller event stacks when they
    are switched to, if they want to receive other events (e.g. from the model)
    they must manage that themselves.

    """

    __metaclass__ = ModeMeta

    #: The name used to key the mode in the mode directory.
    name = None

    #: The renderer class to instantiate for handlers.
    renderer = Renderer

    def __init__(self):
        """Construct a Mode object.

        """
        self.keys = key.KeyStateHandler()
        if self.renderer is not None:
            self.renderer = self.renderer(self)

    def connect(self, control):
        """Respond to the connecting controller.

        :Parameters:
            `control` : Controller
                The connecting Controller object.

        """
        self.control = control
        self.window = control.window
        self.window.push_handlers(self.keys)
        self.window.push_handlers(self.renderer)

    def disconnect(self):
        """Respond to the disconnecting controller.

        """
        self.window.remove_handlers(self.renderer)
        self.window.remove_handlers(self.keys)
        self.window = None
        self.control = None

    def tick(self):
        """Process a single tick.

        """

    def update(self, dt):
        """Update real time components.

        :Parameters:
            `dt` : float
                The actual time that has passed since the last tick.

        """
