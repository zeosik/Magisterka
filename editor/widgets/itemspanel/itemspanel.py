import gi

from editor.widgets.itemspanel.listbox import ListBox

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from editor.widgets.itemspanel.listboxheader import ListBoxHeader


class ItemsPanel(Gtk.VBox):

    def __init__(self, header_name):
        Gtk.VBox.__init__(self)

        self.header = ListBoxHeader(header_name)
        self.pack_start(self.header, False, False, 0)

        self.list_box = ListBox()
        self.pack_start(self.list_box, True, True, 0)
