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
        
        if not self._checkDTavailable():
            print "Way to create new device_type and new udev rules (coding)"
            sys.exit(0) #temporally, waiting for code
        
        self.dev_type_conf=DeviceTypeConf(self.dev_type)
        self._notify(self.dev_type_conf.getNotify())
   
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

    def _notify(self, message):
        notify = pynotify.Notification("HANS notification", message)
        notify.set_urgency(pynotify.URGENCY_CRITICAL)
        notify.set_category("device")
        
        if not notify.show():
            print "Failed to send notification"
            

class DeviceTypeConf():
        
    def __init__(self, dev_type):
        self.config = ConfigParser.ConfigParser()
        self.config.read(HANS_PATH_DB+dev_type+".ini")
        self.notify = self.config.get(dev_type, "notify")
        self.icon_notify = self.config.get(dev_type, "icon-notify")
        self.action = self.config.get(dev_type, "action")
        self.recommend_pkg = self.config.get(dev_type, "recommned-pkg")
        
    def getNotify(self):
        return self.notify

    def getIconNotify(self):
        return self.icon_notify
   
    def getAction(self):
        return self.action

    def getRecommendPkg(self):
        return self.recommend_pkg


def usage():
    print "Usage: hans-core.py [-t|--type] [-p|--path]" 

if __name__ == '__main__':
    hans=HansCore()
    hans.main(sys.argv[1:])
