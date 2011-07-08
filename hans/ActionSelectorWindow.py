# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from hans.helpers import get_builder

import gettext
from gettext import gettext as _

gettext.textdomain('hans')

class ActionSelectorWindow(gtk.Window):
    __gtype_name__ = "ActionSelectorWindow"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated EditlauncherDialog object.
        """
        builder = get_builder('ActionSelectorWindow')
        new_object = builder.get_object('actionselector_window')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a EditlauncherDialog object with it in order to
        finish initializing the start of the new EditlauncherDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    
    def on_btexec_clicked(self, widget, data=None):
        pass

    def on_btcancel_clicked(self, widget, data=None):
        gtk.main_quit()

    def on_destroy(self, widget, data=None):
        """Called when the PlauncherWindow is closed."""
        # Clean up code for saving application state should be added here.
        gtk.main_quit()
    

if __name__ == "__main__":
    dialog = ActionSelectorWindow()
    dialog.show()
    gtk.main()
