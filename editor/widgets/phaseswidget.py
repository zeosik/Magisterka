import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.phase import Phase
from editor.widgets.itemspanel.itemspanel import ItemsPanel


class PhasesWidget(ItemsPanel):

    def __init__(self):
        ItemsPanel.__init__(self, 'List of Phases')

        self.next_phase_index = 1
        self.phases = []

        add_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_button.connect('clicked', self.add_phase)

        self.header.add_button(add_button)

    def add_phase(self, button):
        name = 'Phase-' + str(self.next_phase_index)
        self.next_phase_index += 1
        phase = Phase(name)
        self.phases.append(phase)

        self.list_box.add_item(phase.name)
