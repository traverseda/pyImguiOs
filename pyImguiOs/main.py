# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import pyglet
from pyglet import gl
import traceback

import imgui
from imgui.integrations.pyglet import PygletRenderer

from core import Desktop, mainWindow, alerts
from plugins import get_app_list

app_list = list(get_app_list())
desktop = Desktop()

from apps.alerts import ExceptionAlert
from menuWidgets import Clock, BatteryMonitor
clock = Clock()
battery = BatteryMonitor()

def main():
    window = mainWindow
    gl.glClearColor(0.5, 0.5, 0.5, 1)
    imgui.create_context()
    impl = PygletRenderer(window)

    def update():
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("System", True):
                for app in app_list:
                    clicked, selected = imgui.menu_item(app.__name__,'', False, True)
                    if clicked: desktop.add(app())
                imgui.separator()
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", '', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.text("|")
            battery.render()
            imgui.text("|")
            clock.render()
            imgui.end_main_menu_bar()
        desktop.render()

    @window.event
    def on_draw():
        update()
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    while True:
        try:
            pyglet.app.run()
        except Exception as e:
            if isinstance(e, imgui.core.ImGuiError):
                raise e
            else:
                alert = ExceptionAlert(repr(e),str(traceback.format_exc()))
                alerts.update((alert,))
                traceback.print_exc()
    impl.shutdown()

if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        pass

