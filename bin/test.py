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

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from hans import (
    ActionLauncher, ActionSelectorSimple, ActionSelectorDialog, SimpleActionSelectorWindow, actions
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


def execute_callback(button, dialog):

    selected_interface = dialog.get_selected_interface()
    selected_actions = dialog.get_selected_actions()
    set_as_default = dialog.get_set_as_default()
    #dialog.destroy()

    print selected_interface
    print selected_actions
    print set_as_default

    if set_as_default:
        de = dialog.device.get_defaults_entry()
        de.setInterface(selected_interface.getName())
        de.setActions(';'.join(selected_actions))
        de.write()

    if isinstance(selected_interface, InterfaceEntry.InterfaceEntry):
        launch_actions(selected_interface, selected_actions)

def launch_actions(interface_entry, action_list):

    launcher = ActionLauncher.ActionLauncher(interface_entry)
    launcher.execute(action_list)

if __name__ == "__main__":

    try:
        syspath = '/sys/devices/pci0000:00/0000:00:1d.7/usb1/1-5'
        device = DeviceClass.DeviceClass(syspath)

        #dialog = ActionSelectorDialog.ActionSelectorDialog(device, execute_callback)
        #dialog.main()

        dialog = ActionSelectorSimple.ActionSelectorSimple(device, execute_callback)
        dialog.main()

    except Exception, e:
        print e

