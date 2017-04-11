import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GameCharts(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.generalChart = Gtk.VBox()
        self.generalChart.pack_start(Gtk.Label("Upper Chart"), False, False, 5)
        self.pack_start(self.generalChart, True, True, 0)

        self.detailedChart = Gtk.VBox()
        self.detailedChart.pack_start(Gtk.Label("Lower Chart"), False, False, 5)
        self.pack_start(self.detailedChart, True, True, 0)
