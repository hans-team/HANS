# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (c) 2011 Junta de Andalucia
#
# Authors:
#    Antonio Hernández <ahernandez at emergya.com>
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


import shlex
import subprocess

def get_instance(action_entry):
    return DefaultAction(action_entry)

class DefaultAction():

    def __init__(self, action_entry):
        self._action_entry = action_entry

    def execute(self, udev_item):
        try:
            cmd = self._action_entry.get_exec()
            args = shlex.split(cmd)
            p = subprocess.Popen(args)

        except Exception, e:
            raise e
