import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.phase import Phase
from editor.widgets.itemspanel.itemspanel import ItemsPanel


class PhasesWidget(ItemsPanel):

    def __init__(self, mediator):
        ItemsPanel.__init__(self, 'List of Phases', mediator.phases.remove.fire, mediator.phases.select.fire)

        self.next_phase_index = 1

        self.mediator = mediator
        self.mediator.players.add.register(self.clear_selection)
        self.mediator.players.select.register(self.clear_selection)
        self.mediator.phases.add.register(self.on_phase_add)

        add_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_phase)

        self.header.add_button(add_button)

    def add_phase(self, button):
        name = 'Phase-' + str(self.next_phase_index)
        self.next_phase_index += 1
        self.mediator.phases.add.fire(self, Phase(name))

    def on_phase_add(self, sender, phase):
        self.list_box.add_item(phase, phase.name)

    def clear_selection(self, sender, value):
        self.list_box.clear_selection()
