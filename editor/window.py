import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EditorWindow(Gtk.Window):
    def __init__(self, geometry = (400, 500)):
        Gtk.Window.__init__(self, title="Editor")

        self.set_default_size(geometry[0], geometry[1])

        self.connect("delete-event", Gtk.main_quit)


def run():
    editor = EditorWindow()
    editor.show_all()
    Gtk.main()