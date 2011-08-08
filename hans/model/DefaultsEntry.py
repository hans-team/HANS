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

from xdg.IniFile import *
import os
import types
from hans import utils

class DefaultsEntry(IniFile):

    defaultGroup = 'Defaults Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(os.path.join(utils.get_defaults_path(), filename))

    def __str__(self):
        return self.get_name()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, file):
        IniFile.parse(self, file, [self.defaultGroup])

    def write(self):
        IniFile.write(self, self.filename)

    # start standard keys
    def get_interface(self):
        return self.get('Interface')
    def set_interface(self, interface):
        self.set('Interface', interface)

    def get_actions(self):
        return self.get('Actions')
    def set_actions(self, actions):
        self.set('Actions', actions)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.defaultGroup)
        self.filename = os.path.join(utils.get_defaults_path(), filename)
