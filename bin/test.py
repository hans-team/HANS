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
import threading

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'hans'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from hans import (
    HansThread, ActionLauncher, ActionSelectorSimple, ActionSelectorDialog, actions
)

from hans.model import (DeviceClass, InterfaceClass, InterfaceEntry, DefaultsEntry)

HANS_PATH_DB = PROJECT_ROOT_DIRECTORY + '/db'
HANS_PATH_ACTIONS_DB = HANS_PATH_DB + '/actions'
TEXTBUFFER_LOGGER = 'hans-core'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'



if __name__ == "__main__":

    sysfspath = '/sys/devices/pci0000:00/0000:00:1d.7/usb1/1-5'
    device = DeviceClass.DeviceClass(sysfspath)

    t = HansThread.HansThread(device)
    t.start()

