#!/usr/bin/python

import gtk
import types
import gettext
from gettext import gettext as _

from hans.helpers import get_builder
from hans import InterfaceEntry

gettext.textdomain('plauncher')

class SimpleActionSelectorWindow(gtk.Window):

    __gtype_name__ = "SimpleActionSelectorWindow"

    def __init__(self, device=None, execute_callback=None):
        gtk.Window.__init__(self)

    def main(self):
        gtk.main()

    def __new__(cls, device=None, execute_callback=None):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        """
        builder = get_builder('SimpleActionSelector')
        new_object = builder.get_object('SimpleActionSelectorWindow')
        new_object.finish_initializing(builder, device, execute_callback)
        return new_object

    def finish_initializing(self, builder, device, execute_callback):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a SimpleActionSelectorWindow object with it in order to
        finish initializing the start of the new SimpleActionSelectorWindow
        instance.
        """

        self.iconviewActions = builder.get_object('iconviewActions')
        self.lblDescription = builder.get_object('lblDescription')
        self.btnClose = builder.get_object('btnClose')

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.device = device
        self._action_name_map = None

        self.builder.connect_signals(self)
        #if type(execute_callback) == types.FunctionType:
        #    self.btnExecute.connect('clicked', execute_callback, self)

        self._init_iconview()
        self._load_actions()
        self.show()

    def on_deleteEvent(self, widget, data=None):
        gtk.main_quit()

    def on_btnCloseClicked(self, button):
        self.destroy()

    def _init_iconview(self):

        store = gtk.ListStore(str, gtk.gdk.Pixbuf)

        self.iconviewActions.set_model(store)
        self.iconviewActions.set_text_column(0)
        self.iconviewActions.set_pixbuf_column(1)
        self.iconviewActions.set_selection_mode(gtk.SELECTION_SINGLE)

    def _get_action_icon(self, action):
        image = gtk.Image()
        image.set_from_file(action.getIcon())
        return image.get_pixbuf().scale_simple(140, 140, gtk.gdk.INTERP_BILINEAR)

    def _load_actions(self):

        store = self.iconviewActions.get_model()
        store.clear()
        self._action_name_map = {}

        ifaces = self.device.get_interfaces()
        for iface in ifaces:
            #iface = iface.getInterfaceEntry()

            action_list = iface.get_actions()

            for name in action_list:
                action = action_list[name]
                self._action_name_map[action.getName()] = name
                store.append([action.getName(), self._get_action_icon(action)])

        self.iconviewActions.set_model(store)

