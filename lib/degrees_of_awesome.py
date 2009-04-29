import mode
from pyglet.window import key

from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
import pyglet

BAR_HEIGHT = 55

class AwesomeRenderer(mode.Renderer):
    bar = pyglet.image.load('resources/achievement_bar.png')
    amsterdam = None
    
    def __init__(self, handler):
        mode.Renderer.__init__(self, handler)
        pyglet.font.add_file('resources/amsterdam.ttf')
        self.amsterdam = pyglet.font.load('Amsterdam Graffiti', 50)

    def on_draw(self):
        self.handler.window.clear()
        backdrop = pyglet.image.load('resources/non_gomfl_background.png')
        backdrop.blit(0, 0)
        
        for i in range(10):
            self.bar.blit(50, 520 - i * BAR_HEIGHT)

        #glyphs = self.amsterdam.get_glyphs('Just a test')
        #pyglet.font.GlyphString("Just a test", glyphs, 40, 200).draw()
        pyglet.font.Text(self.amsterdam, "Here is the test", 60, 320, color=(0,0,0,1)).draw()
                    
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
