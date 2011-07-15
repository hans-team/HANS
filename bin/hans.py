#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4 
# vim: expandtab
###
#
# Copyright (c) 2011 David Amián
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : David Amián <damian@emergya.com>
# 
###
import sys
import getopt
import logging
import os

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses


from hans import (_, utils, ActionSelectorSimple, ActionLauncher)
from hans.model import (DeviceClass, InterfaceClass, InterfaceEntry, DefaultsEntry)
from hans.utils import notify

class HansCore():

    def __init__(self, device_path):
        self.device_path = device_path

    def main(self):

        logging.debug(_('Reading device %s') % self.device_path)
        print _('Reading device %s') % self.device_path
        self.device = DeviceClass.DeviceClass(self.device_path)

        notify("HANS - %s" % (_("New device connected",)), self.device.get_formated_name(), self.device.get_pixbuf())

        defaults = self.device.get_defaults_entry()
        action_list = defaults.get_actions()

        if len(action_list) != 0:
            interface_filename = defaults.get_interface()
            interface_entry = InterfaceEntry.InterfaceEntry(interface_filename)
            action_list = action_list.split(';')
            self.launch_actions(interface_entry, action_list)

        else:
            dialog = ActionSelectorSimple.ActionSelectorSimple(self.device, self.on_actionExecuted)
            dialog.main()

    def on_actionExecuted(self, button, dialog):

        selected_interface = dialog.get_selected_interface()
        selected_actions = dialog.get_selected_actions()
        set_as_default = dialog.get_set_as_default()
        #dialog.destroy()

        logging.debug('--------------------')
        logging.debug(selected_interface)
        logging.debug(selected_actions)
        logging.debug(set_as_default)
        logging.debug('--------------------')

        if set_as_default:
            de = dialog.device.get_defaults_entry()
            de.set_interface(selected_interface.get_name())
            de.set_actions(';'.join(selected_actions))
            de.write()

        if isinstance(selected_interface, InterfaceEntry.InterfaceEntry):
            self.launch_actions(selected_interface, selected_actions)

    def launch_actions(self, interface_entry, action_list):
        launcher = ActionLauncher.ActionLauncher(interface_entry)
        launcher.execute(action_list)


def usage():
    print "Usage: hans-core.py [-p|--path]"


if __name__ == '__main__':

    argvs = sys.argv[1:]

    try:
        options, remainder = getopt.gnu_getopt(argvs, 'p:', ['path=', ])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if not options:
        usage()
        sys.exit(2)

    optpath = False
    device_path = None

    for opt, arg in options:
        if opt in ('-p', '--path'):
            optpath = True
            device_path = arg


    if not optpath :
        print "[-p|--path] option is required"
        usage()
        sys.exit(2)

    hans = HansCore(device_path)
    hans.main()
