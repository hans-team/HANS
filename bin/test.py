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

def usage():
    print "Usage: hans-core.py [-p|--path]"

if __name__ == "__main__":
    
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'p:', [
                                                             'path=',
                                                             ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if not options:
        usage()
        sys.exit(2)

    optpath = False

    for opt, arg in options:
        if opt in ('-p', '--path'):
            optpath = True
            path_dev = arg


    if not optpath :
        print "[-p|--path] option is required"
        usage()
        sys.exit(2)
    #if pid == 0:
    sysfspath = path_dev
    print os.path.expanduser('~')
    print sysfspath
    device = DeviceClass.DeviceClass(sysfspath)

#    notify("HANS - New "+device.get_device_type()+" connected ", device.get_formated_name(), device.get_pixbuf())

 #   dialog = ActionSelectorSimple.ActionSelectorSimple(device, on_actionExecuted)
 #   dialog.main()

    #gobject.MainLoop().run()
    
    #except Exception, e:
    #    print e
    t = HansThread.HansThread(device)
    #t.start()
    t.run()
    #else:
     #   os._exit(0)
