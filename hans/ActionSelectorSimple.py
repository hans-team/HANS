# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk
import pango
import types
import gobject

from hans.helpers import get_builder

import gettext
from gettext import gettext as _

gettext.textdomain('hans')

class ActionSelectorSimple(gtk.Window):
    __gtype_name__ = "ActionSelectorSimple"

    def __init__(self, device=None, execute_callback=None):
        gtk.Window.__init__(self)

    def main(self):
        gtk.main()

    def __new__(cls, device=None, execute_callback=None):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated ActionSelectorSimple object.
        """
        builder = get_builder('ActionSelectorSimple')
        new_object = builder.get_object('actionselector_simple')
        new_object.finish_initializing(builder, device, execute_callback)
        return new_object

    def finish_initializing(self, builder, device, execute_callback):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ActionSelectorSimple object with it in order to
        finish initializing the start of the new ActionSelectorSimple
        instance.
        """

        self.iconviewInterfaces = builder.get_object('iconviewInterfaces')
        self.iconviewActions = builder.get_object('iconviewActions')
        self.lblTitle = builder.get_object('lblTitle')

        title = 'HANS: %s %s' % (_('Actions for device'), device.getName())
        title = '<big><big><b>%s</b></big></big>' % (title,)
        self.lblTitle.set_markup(title)

        self.set_title('HANS %s' % (_('Action selector'),))

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.device = device
        self.interface = None
        self._action_name_map = None

        self.builder.connect_signals(self)
        if type(execute_callback) == types.FunctionType:
            self.connect('execute-action', execute_callback)

        self._init_iconview(self.iconviewInterfaces)
        self._init_iconview(self.iconviewActions)
        self._load_interfaces()

        self.show()

    def get_selected_device(self):
        return self.device

    def get_selected_interface(self):
        return self._get_selected_iconview_item(self.iconviewInterfaces)

    def get_selected_actions(self):
        action = self._get_selected_iconview_item(self.iconviewActions)
        if action == None:
            return ()
        name = self._action_name_map[action.getName()]
        action_list = (name,)
        return action_list

    def get_set_as_default(self):
        return False

    def on_destroy(self, widget, data=None):
        """Called when the ActionSelectorSimple is closed."""
        # Clean up code for saving application state should be added here.
        gtk.main_quit()

    def on_iconviewActions_changed(self, iconview):
        try:
            action = self._get_selected_iconview_item(iconview)
            self.emit('execute-action', self)

        except Exception, e:
            print 'on_iconviewActions_changed', e
            pass

    def on_iconviewInterfaces_changed(self, iconview):
        try:
            self.interface = self._get_selected_iconview_item(iconview)
            self._load_actions(self.interface)

        except Exception, e:
            print 'on_iconviewInterfaces_changed', e
            pass

    def _get_selected_iconview_item(self, iconview):

        item = None

        try:
            cursor = iconview.get_cursor()
            path = cursor[0]
            model = iconview.get_model()
            item = model.get_value(model.get_iter(path), 5)

        except Exception, e:
            print e
            pass

        return item

    def _get_icon(self, entry):
        image = gtk.Image()
        image.set_from_file(entry.getIcon())
        pixbuf = image.get_pixbuf()
        return pixbuf.scale_simple(68, 68, gtk.gdk.INTERP_BILINEAR)

    def _get_text(self, entry):
        return '<b>' + _(entry.getName()) + '</b>'

    def _init_iconview(self, iconview):

        #store = gtk.ListStore(str, gtk.gdk.Pixbuf)

        #iconview.set_model(store)
        #iconview.set_text_column(0)
        #iconview.set_pixbuf_column(1)
        iconview.set_selection_mode(gtk.SELECTION_SINGLE)

    def _load_interfaces(self):

        store = self.iconviewInterfaces.get_model()
        store.clear()

        ifaces = self.device.get_interfaces()
        for iface in ifaces:
            #iface = iface.getInterfaceEntry()
            store.append([
                self._get_icon(iface), self._get_text(iface),
                pango.ALIGN_CENTER, 140, pango.WRAP_WORD,
                iface
            ])

        self.iconviewInterfaces.set_model(store)

    def _load_actions(self, iface):

        store = self.iconviewActions.get_model()
        store.clear()

        self._action_name_map = {}

        action_list = iface.get_actions()
        for name in action_list:
            action = action_list[name]
            self._action_name_map[action.getName()] = name
            store.append([
                self._get_icon(action), self._get_text(action),
                pango.ALIGN_CENTER, 140, pango.WRAP_WORD,
                action
            ])

        self.iconviewActions.set_model(store)


gobject.type_register(ActionSelectorSimple)
gobject.signal_new(
    'execute-action', ActionSelectorSimple,
    gobject.SIGNAL_ACTION, gobject.TYPE_NONE,
    (object,)
)
