import gi

from editor.widgets.special.generalchartwidget import GeneralChartWidget

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GameCharts(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.general_chart = GeneralChartWidget()
        self.pack_start(self.general_chart, True, True, 0)

        self.detailed_chart = Gtk.VBox()
        self.detailed_chart.pack_start(Gtk.Label("Lower Chart"), False, False, 5)
        self.pack_start(self.detailed_chart, True, True, 0)
