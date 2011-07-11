# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# Almost based on arista.inputs module:
# Copyright 2008 - 2010 Daniel G. Taylor <dan@programmer-art.org>
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
# Authors : J. Félix Ontañón <fontanon@emergya.es>
# 

import gobject
import gudev

class UdevSignals(gobject.GObject):
    '''
    An object that will find and monitor devices on your 
    machine and emit signals when are added / removed / changed
    '''

    __gsignals__ = {
        'added': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),
        'removed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),
        'changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),
    }

    def __init__(self, subsystems=[], parent_tree=False):
        '''
        Create a new DeviceFinder and attach to the udev system to 
        listen for events.
        '''
        self.__gobject_init__()

        self.client = gudev.Client(subsystems)
        self.subsystems = subsystems

        self.client.connect('uevent', self.event)


    def event(self, client, action, gudevice):
        '''Handle a udev event'''

        return {
            'add': self.device_added,
            'remove': self.device_removed,
            'change': self.device_changed,
        }.get(action, lambda x,y: None)(gudevice, gudevice.get_subsystem())

    def device_added(self, gudevice, subsystem):
        '''Called when a device has been added to the system'''
        self.emit('added', gudevice)

    def device_removed(self, gudevice, subsystem):
        '''Called when a device has been removed from the system'''
        self.emit('removed', gudevice) 

    def device_changed(self, gudevice, subsystem):
        '''Called when a device has been updated'''
        fin=open("/tmp/signals3","w")
        fin.write(gudevice.get_sysfs_path())
        fin.close()

gobject.type_register(UdevSignals)

