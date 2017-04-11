import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PropertiesPanel(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        label = Gtk.Label("Properties")
        self.pack_start(label, False, False, 5)
