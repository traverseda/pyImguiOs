from pyImguiOs.core import Window, mainWindow
import pyglet
import pty, pyte, imgui, shlex, os, signal
import sys

def render_line(line):
    imgui.text(line)

from threading  import Thread
from queue import Queue, Empty

def enqueue_output(out, queue):
    while True:
        queue.put(out.read(1))
    out.close()

class Vt100(Window):
    """A vt100 terminal emulator based on pyte.
    """
    #ToDo: Add support for coloured text
    #ToDo: Show the cursor
    #ToDo: Implement terminal resizing
    def __init__(self, command="bash"):
        self.screen = pyte.Screen(80, 24)
        self._stream = pyte.ByteStream(self.screen)
        p_pid, master_fd = pty.fork()
        self.pid = p_pid
        argv = shlex.split(command)
        if p_pid == 0:  # Child.
            env=dict(TERM="linux", COLUMNS="80", LINES="24")
            os.execvpe(argv[0], argv, env)
        p_file = os.fdopen(master_fd, "w+b", 0)
        self._p_file=p_file
        self._p_out=Queue(256)
        self._readerThread=Thread(target=enqueue_output, args=(p_file, self._p_out))
        self._readerThread.daemon = True
        self._readerThread.start()
        self.focused=False
        #Hopefully this holds a weakref....
        #ToDo: make sure this isn't keeping instance from being garbage collected
        #ToDo: it is, fix that.
        mainWindow.event(self.on_text_motion)
        mainWindow.event(self.on_text)
        super().__init__()

    def __del__(self):
        print("cleaning up vt100")
        pass

    def on_text(self,text):
        if self.focused:
            self._p_file.write(text.encode())

    def on_text_motion(self,textEvent):
        if self.focused: #ToDo: implement actual motion events
            try:
                self._p_file.write(pyglet_to_vt100[textEvent])
            except KeyError as e:
                name = pyglet.window.key.motion_string(textEvent)
                e.args+= ("Unknown key press: "+name,)
                raise e

    def render(self):
        self.focused=imgui.is_window_focused()
        while not self._p_out.empty():
            self._stream.feed(self._p_out.get())
        tuple(map(render_line,self.screen.display))


#A conversion table for converting pyglet
#key events to their vt100 control equivelent
#https://pyglet.readthedocs.io/en/latest/modules/window_key.html
from pyglet.window import key as k
pyglet_to_vt100 = {
    k.MOTION_BACKSPACE: b'\x08',
}
