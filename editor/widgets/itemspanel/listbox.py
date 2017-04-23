import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from common.game import Game


class ListBox(Gtk.ScrolledWindow):

    def __init__(self, mediator, on_row_select):
        Gtk.ScrolledWindow.__init__(self)

        self.mediator = mediator
        self.list_box = Gtk.ListBox()
        self.list_box.connect('row-activated', lambda lb, row: on_row_select(row.object))
        self.add_with_viewport(self.list_box)

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
        self.list_box.show_all()

    def remove_item(self, button):
        # okropny kawalek kodu, nie mamy obiektu Player/Phase wiec wydobywamy go z nazwy
        item_name = button.row.get_children()[0].get_children()[0].get_text()
        items = []
        if "Phase" in item_name:
            items = Game.phases
        else:
            items = Game.players
        for item in items:
            if item.name == item_name:
                items.remove(item)
        self.list_box.remove(button.row)
        self.mediator.remove_item()
        self.list_box.show_all()

    def clear_selection(self):
        self.list_box.unselect_all()
