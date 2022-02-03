# Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class mainWin(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")

        self.box = Gtk.Box(spacing = 10)
        self.add(self.box)

        self.button1 = Gtk.Button(label = "Click Here")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button1, True, True, 0)
        #self.add(self.button1)

    def on_button1_clicked(self, widget):
        print("hello from button 1")

    def on_button2_clicked(self, widget):
        print("hello from button 2")

win = mainWin()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()
