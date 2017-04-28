import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.phase import Phase
from editor.widgets.itemspanel.itemspanel import ItemsPanel


class PhasesWidget(ItemsPanel):

    def __init__(self, mediator):
        ItemsPanel.__init__(self, 'List of Phases', mediator.phases.remove, mediator.phases.select)

        self.next_phase_index = 1

        self.mediator = mediator
        self.mediator.players.register_add(self.clear_selection)
        self.mediator.players.register_select(self.clear_selection)
        self.mediator.phases.register_add(self.on_phase_add)

        add_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_phase)

        self.header.add_button(add_button)

    def add_phase(self, button):
        name = 'Phase-' + str(self.next_phase_index)
        self.next_phase_index += 1
        self.mediator.phases.add(Phase(name))

    def on_phase_add(self, phase):
        self.list_box.add_item(phase, phase.name)

    def clear_selection(self, p):
        self.list_box.clear_selection()
