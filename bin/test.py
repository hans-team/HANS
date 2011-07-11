#!/usr/bin/python

import sys
import getopt
import logging
import ConfigParser
import string
import pynotify
import os
import re
import time
import gtk
import gudev

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from hans import (ActionLauncher, ActionSelectorSimple, ActionSelectorDialog, actions)

from hans.model import (DeviceClass, InterfaceClass, InterfaceEntry, DefaultsEntry)

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
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'p:', [
                                                             'path=',
                                                             ])
    except getopt.GetoptError:
        sys.exit(2)

    if not options:
        sys.exit(2)

    optpath = False

    for opt, arg in options:
        if opt in ('-p', '--path'):
            optpath = True
            path_dev = arg


    if not optpath :
        print "[-p|--path] option is required"

    fin=open("/tmp/pete2","w") 
    fin.write(path_dev)
    fin.close()

    #try:
    device = DeviceClass.DeviceClass(path_dev)

        #dialog = ActionSelectorDialog.ActionSelectorDialog(device, execute_callback)
        #dialog.main()

    dialog = ActionSelectorSimple.ActionSelectorSimple(device, execute_callback)
    dialog.main()
    
    #except Exception, e:
    #    print e
