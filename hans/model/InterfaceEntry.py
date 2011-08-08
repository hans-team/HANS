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

"""
Complete implementation of the XDG Device Entry Specification Version 1.0

Standard Keys:

Name = Generic name device
Notify = Messenge to notify the system
Icon-Notify = Icon for notification
Action = Action that is associated with the device. Can be run scripts, install libraries, request some information to user...
Recommend-Pkg = This key provides a list of packages that are recommended installed in the system

"""

from xdg.IniFile import *
import os
import re
from hans import utils
from hans.hansconfig import get_data_path
import ActionEntry

DEFAULT_INTERFACE_FILENAME = 'vendor-specific'

class InterfaceEntry(IniFile):
    "Class to parse and validate DesktopEntries"

    default_group = 'Interface Entry'

    def __init__(self, filename=None, udev_object=None):
        self.content = dict()
        self.udev_object = udev_object
        self.parse(os.path.join(utils.get_interfaces_path(), filename + '.interface'))

    def __str__(self):
        return self.get_name()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, filepath):
        if not os.path.exists(filepath):
            filepath = os.path.join(utils.get_interfaces_path(), DEFAULT_INTERFACE_FILENAME + '.interface')
        try:
            IniFile.parse(self, filepath, ["Interface Entry"])
        except Exception, e:
            print e

    def get_interface_class(self):
        return self.udev_object

    def get_actions(self):

        selected_actions = self.get_action().split(';')
        action_path = utils.get_actions_path()
       # action_path = os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'db/actions')
        files = os.listdir(action_path)
        action_list = {}

        for filename in files:
            regexp = re.compile('^(.+)\.(action)$')
            m = regexp.match(filename)
            if m != None:
                groups = m.groups()
                action_name = groups[0]
                #file_path = os.path.join(action_path, filename)
                action_entry = ActionEntry.ActionEntry(filename)
                if action_name in selected_actions:
                    action_list[action_name] = action_entry

        return action_list

    # start standard keys
    def get_name(self):
        return self.get('Name', locale=True)
    def set_name(self, name):
        self.set('Name', name)

    def get_notify(self):
        return self.get('Notify', locale=True)

    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):

        filename = self.get('Icon')

        if not os.path.exists(filename):
            filename = utils.get_theme_icon_path(filename, icon_size, flags)

        if filename == None:
            iclass = self.get_interface_class()
            filename = iclass.get_icon(icon_size, flags)
            if type(filename) == str and not os.path.exists(filename):
                filename = utils.get_theme_icon_path(filename, icon_size, flags)

        if filename == None:
            filename = utils.get_default_icon_interface()

        return filename

    def set_icon(self, icon):
        self.set('Icon', icon)

    def get_pixbuf(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):
        filename = self.get_icon(icon_size, flags)
        pixbuf = utils.get_pixbuf_from_file(filename, icon_size)
        return pixbuf

    def get_action(self):
        return self.get('Action')
    def set_action(self, action):
        self.set('Action', action)

    def get_recommend_pkgs(self):
        return self.get('Recommend-Pkgs', locale=True)
    def set_recommend_pkgs(self, rpkgs):
        self.set('Recommend-Pkgs', rpkgs)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.default_group)
        self.filename = os.path.join(utils.get_interfaces_path(), filename + '.interface')
