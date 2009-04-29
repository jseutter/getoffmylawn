import mode
from pyglet.window import key

from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED

class AwesomeRenderer(mode.Renderer):

    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        
    def on_draw(self):
        self.handler.window.clear()
                
class AwesomeMode(mode.Mode):
    name = "awesome"
    renderer = AwesomeRenderer
    
    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            pass
        elif key.ESCAPE:
            self.control.switch_handler("menu")  
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED
