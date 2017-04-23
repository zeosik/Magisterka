import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.phase import Phase
from common.game import Game
from editor.widgets.itemspanel.itemspanel import ItemsPanel


class PhasesWidget(ItemsPanel):

    def __init__(self, mediator):
        ItemsPanel.__init__(self, 'List of Phases', mediator, mediator.select_phase)

        self.next_phase_index = 1

        self.mediator = mediator
        self.mediator.register_on_player_add_listener(self.clear_selection)
        self.mediator.register_on_player_select_listener(self.clear_selection)
        self.mediator.register_on_phase_add_listener(self.on_phase_add)

        add_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_phase)

        self.header.add_button(add_button)

    def add_phase(self, button):
        name = 'Phase-' + str(self.next_phase_index)
        self.next_phase_index += 1
        self.mediator.add_phase(Phase(name))

    def on_phase_add(self, phase):
        Game.add_phase(phase)
        self.list_box.add_item(phase, phase.name)

    def clear_selection(self, p):
        self.list_box.clear_selection()
