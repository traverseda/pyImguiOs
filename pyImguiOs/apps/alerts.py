from core import Window, alerts, ignoredAlerts, GenericPythonWidget, Widget
import imgui
import traceback
from utils import singleton

@singleton
class ExceptionAlert(Widget):
    def __init__(self,exception,traceback):
        self.exception=exception
        self.traceback=traceback

    def render(self):
        expanded, visible = imgui.collapsing_header(self.exception)
        if expanded:
            imgui.text(self.traceback)

    def __str__(self):
        return self.exception

def render_alert(alert):
    if not alert in ignoredAlerts:
        alert.render()

class AlertViewer(Window):

    def render(self):
        list(map(render_alert, alerts))
