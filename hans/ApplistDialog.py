# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from hans.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('hans')

class ApplistDialog(gtk.Dialog):
    __gtype_name__ = "ApplistDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated ApplistDialog object.
        """
        builder = get_builder('ApplistDialog')
        new_object = builder.get_object('applist_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ApplistDialog object with it in order to
        finish initializing the start of the new ApplistDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    def ok(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        pass

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass


if __name__ == "__main__":
    dialog = ApplistDialog()
    dialog.show()
    gtk.main()
