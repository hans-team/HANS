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
import ConfigParser
import string
import pynotify
import os
import re
from utils import DeviceEntry

import gettext
from gettext import gettext as _
gettext.textdomain('hans')


#HANS_AVAILABLE_DT='@PREFIX@/share/hans/hans-dt-available.conf'
#HANS_PATH_DB='@PREFIX@/share/hans/db/'
HANS_PATH_DB='db/'
HANS_DT_AVAILABLE='hans-dt-available.conf'
TEXTBUFFER_LOGGER = 'hans-core'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'


class HansCore():

    def main(self,argvs):
        try:
            options, remainder = getopt.gnu_getopt(argvs, 't:p:', ['type=', 
                                                             'path=',
                                                             ])
        except getopt.GetoptError:
            usage()
            sys.exit(2)

        if not options:
            usage()
            sys.exit(2)
        
        if not pynotify.init("HANS notification"):
            sys.exit(1)

        opttype=False

        for opt, arg in options:
            if opt in ('-t', '--type'):
                opttype=True
                self.dev_type = arg
            elif opt in ('-p', '-path'):
                self.path_dev = arg
        
        if not opttype:
            print "[-t|--type] options is required"
            usage()
            sys.exit(2)
        
        regexp = re.compile('[a-z]+-[a-z]+')
        if not regexp.match(self.dev_type):
            print "The device type must be device-'name_of_device'"
            sys.exit(1)

        self.device = self.dev_type.split("-")[1]
        if not self._checkDTavailable():
            self._notify(self.device, _("The device '"+self.device+"' isn't controlled by HANS"))
            print "Way to create new device_type and new udev rules (coding)"
            sys.exit(0) #temporally, waiting for code
        
        self.filename_entry=HANS_PATH_DB+self.device+".device"
        if os.path.exists(self.filename_entry):
            self.dev_type_entry=DeviceEntry.DeviceEntry(self.filename_entry)
        else:
            self._notify(self.device, _("The device '"+self.device+"' hasn't associated entry file"))
            print "Way to create new entry for "+self.device+" by user (coding)"
            sys.exit(0) #temporally, waiting for code
        self._notify(self.device, self.dev_type_entry.getNotify())
   
    def _checkDTavailable(self):
        infile = open(HANS_DT_AVAILABLE, 'r')
        hans_dt_available = list()
        for line in infile:
            hans_dt_available.append(line.strip('\n'))
        infile.close()
        if self.dev_type in hans_dt_available:
            return True
        else:
            return False

    def _notify(self, device,  message):
        notify = pynotify.Notification("HANS notification - "+device, message)
        notify.set_urgency(pynotify.URGENCY_CRITICAL)
        notify.set_category("device")
        
        if not notify.show():
            print "Failed to send notification"
            


def usage():
    print "Usage: hans-core.py [-t|--type] [-p|--path]" 

if __name__ == '__main__':
    hans=HansCore()
    hans.main(sys.argv[1:])
