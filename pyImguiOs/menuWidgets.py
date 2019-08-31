"""A temporay holding cell for menu widgets until
I create a general system for dealing with the menu bar
in an extensible way.
"""
from core import Widget
import imgui

class BatteryMonitor(Widget):
    def __init__(self):
        self.tickrate = 1 #How often do we update battery information

from datetime import datetime
class Clock(Widget):
    def __init__(self,datestring="%Y/%m/%d, %H:%M:%S"):
        self.tickrate = 1
        self.datestring=datestring
        self.update(0)

    def update(self, dt):
        self.timestr=datetime.now().strftime(self.datestring)

    def render(self):
        imgui.text(self.timestr)
