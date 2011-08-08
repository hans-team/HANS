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

class FilechooserDialog(gtk.Dialog):
    __gtype_name__ = "FilechooserDialog"

    def __new__(cls, option):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated FilechooserDialog object.
        """
        builder = get_builder('FilechooserDialog')
        new_object = builder.get_object('filechooser_dialog')
        new_object.finish_initializing(builder, option)
        return new_object

    def finish_initializing(self, builder, option):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a FilechooserDialog object with it in order to
        finish initializing the start of the new FilechooserDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
        self.filech=self.builder.get_object("filechooserwidget")
        if option=="icon":
            self.filter = gtk.FileFilter()
            self.filter.set_name(_("Images file"))
            self.filter.add_mime_type("image/png")
            self.filter.add_mime_type("image/jpeg")
            self.filter.add_pattern("*.png")
            self.filter.add_pattern("*.jpg")
            self.filech.add_filter(self.filter)

            self.filter = gtk.FileFilter()
            self.filter.set_name(_("All files"))
            self.filter.add_pattern("*")
            self.filech.add_filter(self.filter)
            self.filech.preview = gtk.Image()
            self.filech.set_preview_widget(self.filech.preview)
            self.filech.connect("update-preview", update_preview_cb, self.filech.preview)


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

def update_preview_cb(file_chooser, preview):
    filename = file_chooser.get_preview_filename()
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
        preview.set_from_pixbuf(pixbuf)
        have_preview = True
    except:
        have_preview = False
    file_chooser.set_preview_widget_active(have_preview)
    return



if __name__ == "__main__":
    dialog = FilechooserDialog()
    dialog.show()
    gtk.main()
