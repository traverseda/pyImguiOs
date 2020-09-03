"""A temporay holding cell for menu widgets until
I create a general system for dealing with the menu bar
in an extensible way.
"""
from .core import Widget
import imgui
import psutil
import datetime
from datetime import timedelta
from .theme import theme

class BatteryMonitor(Widget):
    def __init__(self):
        self.tickrate = 1 #How often do we update battery information
        self.update(0)

    def update(self,dt):
        self.battery = psutil.sensors_battery()
        self.percentLeft = f"{int(self.battery.percent)}%"
        self.timeLeft = str(timedelta(seconds=self.battery.secsleft))

    def render(self):
        imgui.begin_group()
        imgui.text(self.percentLeft)
        if self.battery.power_plugged:
            imgui.text_colored("I",*theme.color("battery_charging","success"))
        imgui.end_group()
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            if not self.battery.power_plugged:
                imgui.text(f"{self.timeLeft}")
            else:
                imgui.text("Battery is charging")
            imgui.end_tooltip()

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
