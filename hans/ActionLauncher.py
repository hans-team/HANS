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

from actions import *

class ActionLauncher:

    def __init__(self, interface_entry):
        self._interface_entry = interface_entry
        self._action_list = interface_entry.get_actions()

    def execute(self, action_list):

        for action_name in action_list:

            if not action_name in self._action_list:
                continue

            try:
                action_entry = self._action_list[action_name]
                action_instance = self._get_action_instance(action_name, action_entry)
                print 'Instance for action "%s": ' % (action_name,), action_instance
                action_instance.execute(self._interface_entry)

            except Exception, e:
                print e

    def _get_action_instance(self, action_name, action_entry):

        try:
            action_name = action_name.capitalize() + 'Action'
            action_module = globals()[action_name]

        except KeyError, e:
            action_name = 'DefaultAction'
            action_module = globals()[action_name]

        action = None

        try:
            action = action_module.get_instance(action_entry)

        except Exception, e:
            raise e

        return action
