#!/usr/bin/python

import gtk
import types
import gettext
from gettext import gettext as _

from hans.helpers import get_builder
from hans import InterfaceEntry

gettext.textdomain('plauncher')

class ActionSelectorDialog(gtk.Window):

    __gtype_name__ = "ActionSelectorDialog"

    def __init__(self, device=None, execute_callback=None):
        gtk.Window.__init__(self)

    def main(self):
        gtk.main()

    def __new__(cls, device=None, execute_callback=None):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        """
        builder = get_builder('ActionSelectorDialog')
        new_object = builder.get_object('ActionSelectorDialog')
        new_object.finish_initializing(builder, device, execute_callback)
        return new_object

    def finish_initializing(self, builder, device, execute_callback):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ActionSelectorDialog object with it in order to
        finish initializing the start of the new ActionSelectorDialog
        instance.
        """

        self.treeviewActions = builder.get_object('treeviewActions')
        #self.lblDescription = builder.get_object('lblDescription')
        self.btnExecute = builder.get_object('btnExecute')
        self.checkDefaultAction = builder.get_object('checkDefaultAction')

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.device = device
        self._selected_interface = None
        self._action_name_map = None

        self.builder.connect_signals(self)
        if type(execute_callback) == types.FunctionType:
            self.btnExecute.connect('clicked', execute_callback, self)

        self._init_treeview()
        self._load_interfaces()
        self.show()

    def on_deleteEvent(self, widget, data=None):
        gtk.main_quit()

    def on_btnExecuteClicked(self, button):
        #self.destroy()
        pass

    def on_btnCancelClicked(self, button):
        self.destroy()

    def on_checkDefaultActionToggled(self, togglebutton):
        pass

    def on_treeviewActionsRowActivated(self, treeview, path, user_param1):
        pass

    def get_set_as_default(self):
        return self.checkDefaultAction.get_active()

    def get_selected_interface(self):
        return self._selected_interface

    def get_selected_actions(self):

        action_list = []
        treeselection = self.treeviewActions.get_selection()
        (model, paths) = treeselection.get_selected_rows()

        for path in paths:
            iter = model.get_iter(path)
            value = model.get_value(iter, 0)
            action_name = self._action_name_map[value.getName()]
            action_list.append(action_name)

        return action_list

    def _init_treeview(self):

        tvcolumn = gtk.TreeViewColumn('Actions')

        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, False)
        tvcolumn.set_cell_data_func(cell, self._render_column_pixbuf)

        cell = gtk.CellRendererText()
        #tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.set_cell_data_func(cell, self._render_column_text)

        self.treeviewActions.append_column(tvcolumn)
        self.treeviewActions.set_search_column(1)

        treestore = gtk.TreeStore(object)
        self.treeviewActions.set_model(treestore)
        self.treeviewActions.set_rubber_banding(True)
        selection = self.treeviewActions.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        #selection.set_select_function(self._selection_callback, None, True)

    def _selection_callback(self, selection, model, path, is_selected, user_data):
        pass

    def _load_interfaces(self):

        box = self.builder.get_object('buttonboxInterfaces')

        ifaces = self.device.get_interfaces()
        for iface in ifaces:
            #iface = iface.getInterfaceEntry()
            button = gtk.Button(label=iface.getName())
            button.connect('clicked', self._load_actions, iface)
            box.add(button)

        box.show_all()

    def _load_actions(self, button, iface):

        self._selected_interface = iface

        treestore = self.treeviewActions.get_model()
        treestore.clear()

        self._action_name_map = {}
        action_list = iface.get_actions()

        for name in action_list:
            action = action_list[name]
            self._action_name_map[action.getName()] = name
            treestore.append(None, [action])

        self.treeviewActions.set_model(treestore)

    def _render_column_pixbuf(self, column, cell, model, iter):
        action = model.get_value(iter, 0)
        image = gtk.Image()
        image.set_from_file(action.getIcon())
        cell.set_property('pixbuf', image.get_pixbuf())

    def _render_column_text(self, column, cell, model, iter):
        action = model.get_value(iter, 0)
        cell.set_property('text', action.getName())

