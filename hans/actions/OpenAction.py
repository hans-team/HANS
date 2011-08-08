# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
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

import gio
import DefaultAction
from .. import ApplicationSelectorWindow

def get_instance(action_entry):
    return OpenAction(action_entry)

class OpenAction(DefaultAction.DefaultAction):

    def execute(self, interface_entry):

        self.interface_entry = interface_entry

        interfacetype = interface_entry.get_interface_class().get_interface_type()
        app_info = gio.app_info_get_default_for_type(interfacetype, False)

        # NOTE: 1 == 1, for now always show the dialog
        if app_info == None or 1 == 1:
            self._open_dialog(interface_entry)

        else:
            self._execute(app_info, interfacetype, False)

    def _open_dialog(self, interface_entry):
        try:
            dialog = ApplicationSelectorWindow.ApplicationSelectorWindow(interface_entry, self.on_actionExecuted)
            dialog.main()

        except Exception:
            import traceback
            traceback.print_exc()

    def on_actionExecuted(self, dialog, app_info):
        self._execute(app_info, dialog.interfacetype, dialog.get_is_default_application())

    def _execute(self, app_info, interfacetype, is_default_application):

        # TODO: What are the parameters to be passed to the application?
        uris = []
        app_info.launch_uris(uris)

        if is_default_application:
            app_info.set_as_default_for_type(interfacetype)

        else:
            app_info.add_supports_type(interfacetype)
