# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    David Amian <damian at emergya.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

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
