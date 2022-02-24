import gi
import time
import asyncio
from threading import Thread
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class PomodoroClockV1(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="My Hello World Program" )
        Gtk.Window.set_default_size(self, 400,325)
        Gtk.Window.set_position(self, Gtk.WindowPosition.CENTER)
        grid = Gtk.Grid()
        textview = Gtk.TextView()
        textbuffer = Gtk.TextBuffer()
        textview.set_buffer(textbuffer)
        textbuffer.set_text("Clock", -1)
        self.textbuffer = textbuffer
        work_button = Gtk.Button(label="Work")
        work_button.connect("clicked", self.work_button_clicked)
        pause_button = Gtk.Button(label="Pause")
        pause_button.connect("clicked", self.pause_button_clicked)
        self.add(grid)
        grid.attach(work_button, 0, 0, 50, 50)
        grid.attach(pause_button, 50, 0, 50, 50)
        grid.attach(textview, 0, 75, 50, 50)
        self.update = None

    def countdown(self, time_in_seconds):
        while time_in_seconds:
            mins, seconds = divmod(time_in_seconds, 60)
            timer_string = '{:02d}:{:02d}'.format(mins, seconds)
            # print(timer_string)
            GLib.idle_add(
                self.textbuffer.set_text, "Clock:\n"+timer_string,
                priority=GLib.PRIORITY_DEFAULT
            )
            time.sleep(1)
            time_in_seconds -= 1

    def work_button_clicked(self, button):
        # asyncio.run(self.countdown(15))
        self.update = Thread(target=self.countdown, args=[1500])
        self.update.setDaemon(True)
        self.update.start()

    def pause_button_clicked(self, button):
        self.update = Thread(target=self.countdown, args=[300])
        self.update.setDaemon(True)
        self.update.start()



window = PomodoroClockV1()
window.connect("delete-event", Gtk.main_quit)
# GObject.threads_init()
window.show_all()
Gtk.main()