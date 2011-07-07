# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from hans.helpers import get_builder

import gettext
from gettext import gettext as _

gettext.textdomain('hans')

class ActionSelectorSimple(gtk.Window):
    __gtype_name__ = "ActionSelectorSimple"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated ActionSelectorSimple object.
        """
        builder = get_builder('ActionSelectorSimple')
        new_object = builder.get_object('actionselector_simple')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ActionSelectorSimple object with it in order to
        finish initializing the start of the new ActionSelectorSimple
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    
    def on_destroy(self, widget, data=None):
        """Called when the ActionSelectorSimple is closed."""
        # Clean up code for saving application state should be added here.
        gtk.main_quit()
    

if __name__ == "__main__":
    dialog = ActionSelectorSimple()
    dialog.show()
    gtk.main()
