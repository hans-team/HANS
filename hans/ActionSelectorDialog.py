#!/usr/bin/python

import gtk

from hans.helpers import get_builder
from hans import InterfaceEntry

import gettext
from gettext import gettext as _

gettext.textdomain('plauncher')

class ActionSelectorDialog(gtk.Dialog):

    __gtype_name__ = "ActionSelectorDialog"

    def __init__(self, iface=None):
        gtk.Dialog.__init__(self)
        self._iface = iface
        self._set_is_default = False

        self._load_actions()

    def __new__(cls, iface=None):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        """
        builder = get_builder('ActionSelectorDialog')
        new_object = builder.get_object('ActionSelectorDialog')
        new_object._treeviewActions = builder.get_object('treeviewActions')
        new_object._lblDescription = builder.get_object('lblDescription')
        new_object._btnExec = builder.get_object('btnExec')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ActionSelectorDialog object with it in order to
        finish initializing the start of the new ActionSelectorDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    def on_checkDefaultActionToggled(self, togglebutton):
        self._set_is_default = togglebutton.get_active()

    def on_btnExecClicked(self, button):
        # TODO: Do something with the get_is_default_action value
        pass

    def on_btnCancelClicked(self, button):
        pass

    def on_treeviewActionsRowActivated(self, treeview, path, user_param1):
        # TODO: Do something with the get_is_default_action value
        self.response(self.get_response_for_widget(self._btnExec))

    def get_is_default_action(self):
        return self._set_is_default

    def get_selected_actions(self):

        action_list = []
        treeselection = self._treeviewActions.get_selection()
        (model, paths) = treeselection.get_selected_rows()

        for path in paths:
            iter = model.get_iter(path)
            value = model.get_value(iter, 0)
            action_list.append(value.getName())

        return action_list

    def _load_actions(self):

        try:
            a = self._treeviewActions
        except Exception, e:
            return

        self._treeviewActions.connect('row-activated', self.on_treeviewActionsRowActivated)
        tvcolumn = gtk.TreeViewColumn('Actions')

        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, False)
        tvcolumn.set_cell_data_func(cell, self._render_column_pixbuf)

        cell = gtk.CellRendererText()
        #tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.set_cell_data_func(cell, self._render_column_text)

        self._treeviewActions.append_column(tvcolumn)
        self._treeviewActions.set_search_column(1)


        treestore = gtk.TreeStore(object)

        action_list = self._iface.get_actions()
        for name in action_list:
            action = action_list[name]
            if action.getInteractive():
                treestore.append(None, [action])

        self._treeviewActions.set_model(treestore)
        self._treeviewActions.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def _render_column_pixbuf(self, column, cell, model, iter):
        action = model.get_value(iter, 0)
        image = gtk.Image()
        image.set_from_file(action.getIcon())
        cell.set_property('pixbuf', image.get_pixbuf())

    def _render_column_text(self, column, cell, model, iter):
        action = model.get_value(iter, 0)
        cell.set_property('text', action.getName())

