import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListBox(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.list_box = Gtk.ListBox()
        self.add_with_viewport(self.list_box)

    def add_item(self, name):
        row = Gtk.ListBoxRow()
        row_hbox = Gtk.HBox()

        label = Gtk.Label(name)
        label.set_alignment(0, 0.5)
        row_hbox.pack_start(label, True, True, 5)

        remove_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_DELETE))
        remove_button.row = row
        remove_button.connect('clicked', self.remove_item)
        row_hbox.pack_start(remove_button, True, True, 0)

        row.add(row_hbox)

        self.list_box.add(row)
        self.list_box.show_all()

    def remove_item(self, button):
        self.list_box.remove(button.row)
        self.list_box.show_all()
