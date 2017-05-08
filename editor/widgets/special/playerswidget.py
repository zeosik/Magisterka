import gi

from editor.namegenerator.name_generator import NameGenerator

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.playergroup import PlayerGroup
from editor.widgets.itemspanel.itemspanel import ItemsPanel


class PlayersWidget(ItemsPanel):
    def __init__(self, mediator):
        ItemsPanel.__init__(self, 'List of Players', mediator.players_groups.remove.fire, mediator.players_groups.select.fire)

        self.name_generator = NameGenerator('Team')

        self.mediator = mediator
        self.mediator.players_groups.add.register(self.on_player_add)
        self.mediator.phases.add.register(self.clear_selection)
        self.mediator.phases.select.register(self.clear_selection)

        add_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_player_button_click)

        self.header.add_button(add_button)

    def add_player_button_click(self, button):
        player = PlayerGroup(self.name_generator.next_name())
        self.mediator.players_groups.add.fire(self, player)

    def on_player_add(self, sender, player):
        self.list_box.add_item(player, player.name)

    def clear_selection(self, sender, value):
        self.list_box.clear_selection()
