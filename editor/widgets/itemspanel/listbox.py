import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListBox(Gtk.ScrolledWindow):

    def __init__(self, on_row_remove, on_row_select):
        Gtk.ScrolledWindow.__init__(self)

        self.on_row_remove = on_row_remove

        self.list_box = Gtk.ListBox()
        self.list_box.connect('row-activated', lambda lb, row: on_row_select(self, row.object))
        self.add_with_viewport(self.list_box)
        self.rows = []

    def add_item(self, object, display_name):
        row = Gtk.ListBoxRow()
        row_hbox = Gtk.HBox()

        label = Gtk.Label(display_name)
        label.set_alignment(0, 0.5)
        row_hbox.pack_start(label, True, True, 5)

        remove_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_DELETE))
        remove_button.row = row
        remove_button.connect('clicked', self.remove_item)
        row_hbox.pack_start(remove_button, True, True, 0)

        row.add(row_hbox)
        row.object = object

        self.list_box.add(row)
        self.rows.append(row)
        self.list_box.show_all()

    def remove_item(self, button):
        self.list_box.remove(button.row)
        self.list_box.show_all()
        self.on_row_remove(self, button.row.object)

    def clear_selection(self):
        self.list_box.unselect_all()

    def clear_items(self):
        for row in self.rows:
            self.list_box.remove(row)
        self.rows.clear()
