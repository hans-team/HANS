# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    Antonio Hernández <ahernandez at emergya.com>
#    David Amian <damian at emergya.com>
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

import sys
import os.path
from hans import utils
import gudev
import InterfaceEntry
import re
import sys

class InterfaceClass():

    def __init__(self, sysfspath):
        self.sysfspath = sysfspath
        self.client = gudev.Client('usb')
        self.int_udev = self.client.query_by_sysfs_path(sysfspath)
        self.int_entry = InterfaceEntry.InterfaceEntry(self.get_interface_name(), self)

    def __str__(self):
        return self.get_formated_name()

    def get_udev_object(self):
        return self.int_udev

    def get_formated_name(self):
        inttype = self.get_interface_type()
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(str(inttype)):
            print "The device type must be x-usb-device/'name_of_device'"
            print str(inttype)
            sys.exit(1)

        inttype = inttype.split("/")[1].replace('-', ' ').capitalize()
        return inttype

    def get_interface_name(self):
        inttype = self.get_interface_type()
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(str(inttype)):
            print "The device type must be x-usb-device/'name_of_device'"
            print str(inttype)
            sys.exit(1)

        return inttype.split("/")[1]

    def get_interface_type(self):
        inttype = self.int_udev.get_property('INTERFACETYPE')
        return inttype

    def get_interface_entry(self):
        return self.int_entry

    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):
        filename = None
        l_udev = self.client.query_by_subsystem('*')
        for udev_object in l_udev:
            if self.sysfspath + '/' in udev_object.get_sysfs_path():
                filename = udev_object.get_property('ICON')
                if filename:
                    if not os.path.exists(filename):
                        filename = utils.get_theme_icon_path(filename, icon_size, flags)
                    return filename

        return filename

