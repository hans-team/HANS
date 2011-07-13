#!/usr/bin/python

import sys
import logging
import os


# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from hans import _, ActionLauncher, ActionSelectorSimple
from hans.model import (DeviceClass, InterfaceClass, InterfaceEntry, DefaultsEntry)
from hans.utils import notify

HANS_PATH_DB = PROJECT_ROOT_DIRECTORY + '/db'
HANS_PATH_ACTIONS_DB = HANS_PATH_DB + '/actions'
TEXTBUFFER_LOGGER = 'hans-core'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'


def on_actionExecuted(button, dialog):

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
        launch_actions(selected_interface, selected_actions)

def launch_actions(interface_entry, action_list):
    launcher = ActionLauncher.ActionLauncher(interface_entry)
    launcher.execute(action_list)

if __name__ == "__main__":

    print _('Action selector')

    #sysfspath = '/sys/devices/pci0000:00/0000:00:1d.7/usb1/1-5'
    #device = DeviceClass.DeviceClass(sysfspath)

    #notify("HANS - New device connected", device.get_formated_name(), device.get_pixbuf())

    #dialog = ActionSelectorSimple.ActionSelectorSimple(device, on_actionExecuted)
    #dialog.main()
