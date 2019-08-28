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

def render_alert(alertItem):
    alert, count = alertItem
    if not alert in ignoredAlerts:
        imgui.text(str(count))
        imgui.next_column()
        alert.render()
        imgui.next_column()
        imgui.separator()

class AlertViewer(Window):

    def render(self):
        imgui.columns(2, 'alertList')
        imgui.set_column_offset(1, 45)
        imgui.text("Count")
        imgui.next_column()
        imgui.text("Alert")
        imgui.next_column()
        imgui.separator()
        #ToDo: In the future dont revert this, and simple have it lock scroll
        #to bottom like a terminal? Might be more effort than it's worth.
        list(map(render_alert, reversed(alerts.items())))
        imgui.text("Count")
        imgui.next_column()
        imgui.text("Alert")
        imgui.next_column()
        imgui.columns(1)
