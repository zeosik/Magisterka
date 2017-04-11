import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.player import Player
from editor.widgets.itemspanel.itemspanel import ItemsPanel

names = ['Alice', 'Bob', 'John']


class PlayersWidget(ItemsPanel):

    def __init__(self):
        ItemsPanel.__init__(self, 'List of Players')

        self.next_name_index = 0
        self.players = []

        add_button = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_player)

        self.header.add_button(add_button)

    def add_player(self, button):
        player = Player(names[self.next_name_index])
        self.next_name_index = (self.next_name_index + 1) % len(names)
        self.players.append(player)

        self.list_box.add_item(player.name)
