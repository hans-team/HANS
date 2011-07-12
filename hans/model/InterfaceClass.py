import os.path
from hans import utils
import gudev
import re
import InterfaceEntry
import re

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
        inttype = self.int_udev.get_property('INTERFACETYPE')
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(inttype):
            print "The device type must be x-usb-device/'name_of_device'"
            sys.exit(1)

        inttype = inttype.split("/")[1].replace('-', ' ').capitalize()
        return inttype

    def get_interface_name(self):
        inttype = self.int_udev.get_property('INTERFACETYPE')
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(inttype):
            print "The device type must be x-usb-device/'name_of_device'"
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

