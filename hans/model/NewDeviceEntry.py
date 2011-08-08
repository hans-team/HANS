# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    David Amian <damian at emergya.com>
#    Antonio Hernández <ahernandez at emergya.com>
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
from hans import (InterfaceEntry, FilechooserDialog)

import gettext
from gettext import gettext as _

gettext.textdomain('plauncher')

class NewDeviceEntry(gtk.Dialog):
    __gtype_name__ = "NewDeviceEntry"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated EditlauncherDialog object.
        """
        builder = get_builder('NewDeviceEntry')
        new_object = builder.get_object('newdeviceentry')
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

    
    def on_bticon_clicked(self, widget, data=None):
        chooser = FilechooserDialog.FilechooserDialog("icon")
        response = chooser.run()
        chooser.destroy()

    def on_btcmd_clicked(self, widget, data=None):

       pass 
    
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
    dialog = EditlauncherDialog()
    dialog.show()
    gtk.main()
