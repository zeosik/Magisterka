import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListBoxHeader(Gtk.HBox):
    def __init__(self, name):
        Gtk.HBox.__init__(self)

        label = Gtk.Label(name)
        label.set_alignment(0, 0.5)

        self.pack_start(label, False, False, 5)

    def add_button(self, button):
        self.pack_start(button, False, False, 5)
