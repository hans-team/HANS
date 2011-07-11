#!/usr/bin/python

import sys
import getopt
import logging
import ConfigParser
import string
import pynotify
import os
import re
import gtk
import threading

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from hans import (
    ActionLauncher, ActionSelectorSimple, ActionSelectorDialog, actions
)

from hans.model import (
    DeviceClass, InterfaceClass, InterfaceEntry, DefaultsEntry
)

HANS_PATH_DB = PROJECT_ROOT_DIRECTORY + '/db'
HANS_PATH_ACTIONS_DB = HANS_PATH_DB + '/actions'
TEXTBUFFER_LOGGER = 'hans-core'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'


class HansThread(threading.Thread):
    def __init__(self, sysfspath):
        self.sysfspath = sysfspath
        threading.Thread.__init__(self)

    def run(self):
        #try:
            device = DeviceClass.DeviceClass(self.sysfspath)

            #dialog = ActionSelectorDialog.ActionSelectorDialog(device, execute_callback)
            #dialog.main()

            dialog = ActionSelectorSimple.ActionSelectorSimple(device, self.on_actionExecuted)
            dialog.main()

        #except Exception, e:
        #    print e

    def on_actionExecuted(self, button, dialog):

        selected_interface = dialog.get_selected_interface()
        selected_actions = dialog.get_selected_actions()
        set_as_default = dialog.get_set_as_default()
        #dialog.destroy()

        print '--------------------'
        print selected_interface
        print selected_actions
        print set_as_default
        print '--------------------'

        if set_as_default:
            de = dialog.device.get_defaults_entry()
            de.setInterface(selected_interface.get_name())
            de.setActions(';'.join(selected_actions))
            de.write()

        if isinstance(selected_interface, InterfaceEntry.InterfaceEntry):
            self.launch_actions(selected_interface, selected_actions)

    def launch_actions(self, interface_entry, action_list):

        launcher = ActionLauncher.ActionLauncher(interface_entry)
        launcher.execute(action_list)


if __name__ == "__main__":

    sysfspath = '/sys/devices/pci0000:00/0000:00:1d.7/usb1/1-5'

    t = HansThread(sysfspath)
    t.start()

