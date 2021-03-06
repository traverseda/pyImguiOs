import pyglet, imgui, collections, blinker

windowClosed = blinker.signal("windowClosed")

import operator
call_render = operator.methodcaller('_render')

def render_all(iterable):
    """Quickly calls the _render method on an iterable
    of renderables.
    """
    collections.deque(map(call_render,iterable))

class Desktop:
    def __init__(self):
        self.running=set()
        self.to_add=set()
        self.to_remove=set()
        windowClosed.connect(self.remove)

    def render(self):
        #We need to batch all changes to the beggining of the
        #render call, or the iterables size can change mid-stream
        if self.to_remove:
            self.running.difference_update(self.to_remove)
            self.to_remove.clear()
        if self.to_add:
            self.running.update(self.to_add)
            self.to_add.clear()
        render_all(self.running)

    def add(self, item):
        self.to_add.add(item)

    def remove(self, item):
        self.to_remove.add(item)

class Widget:
    def __init__(self):
        pass

    @property
    def tickrate(self): return getattr(self, "_tickrate", None)

    @tickrate.setter
    def tickrate(self,tickrate):
        #ToDo, this holds a reference to closed windows
        self._tickrate = tickrate
        pyglet.clock.unschedule(self.update)
        if tickrate==None:
            return
        if type(tickrate) == bool and tickrate:
            pyglet.clock.schedule_interval(self.update)
            return
        pyglet.clock.schedule_interval(self.update,tickrate)

    def _render(self):
        self.render()

    def render(self):
        pass

    def update(self,dt):
        pass

windowCount = collections.Counter()

from contextlib import contextmanager
class Window(Widget):
    inAppMenu=True #Set to false if you want the app not to show up in app the "start menu".

    def __init__(self):
        #Get a unique name for this window
        self.name = getattr(self,'name',self.__class__.__name__)
        self._id = windowCount[self.name]
        self._idStr = "{}: {}".format(self._id, self.name)
        windowCount.update((self.name,))
        super().__init__()

    def __enter__(self):
        expanded, opened = imgui.begin(self._idStr, closable=True)
        if not opened: windowClosed.send(self)
        return expanded

    def __exit__(self, type, value, traceback):
        imgui.end()

    def _render(self):
        with self as running:
            if running: self.render()

mainWindow = pyglet.window.Window(width=1280, height=720, resizable=True, vsync=True)
print(mainWindow)

from collections import Counter, OrderedDict
ignoredAlerts = set()
class OrderedAlertCounter(Counter, OrderedDict):
    pass

alerts = OrderedAlertCounter()

