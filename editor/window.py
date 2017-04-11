import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from editor.widgets.playerswidget import PlayersWidget
from editor.widgets.phaseswidget import PhasesWidget


MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <menu id="app-menu">
        <section>
            <item>
                <attribute name="action">app.quit</attribute>
                <attribute name="label" translatable="yes">_Quit</attribute>
                <attribute name="accel">&lt;Primary&gt;q</attribute>
            </item>
        </section>
    </menu>
</interface>
"""


class EditorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, title='Editor', application=app)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.left_panel = Gtk.VBox()
        self.players_widget = PlayersWidget()
        self.left_panel.pack_start(self.players_widget, True, True, 0)

        self.phases_widget = PhasesWidget()
        self.left_panel.pack_start(self.phases_widget, True, True, 0)

        self.add(self.left_panel)


class EditorApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = EditorWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object('app-menu'))

    def on_quit(self, action, param):
        self.quit()


def run():
    app = EditorApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
