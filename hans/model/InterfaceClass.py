import os.path
import gudev
import InterfaceEntry

class InterfaceClass():


    def __init__(self, sysfspath):
        self.sysfspath=sysfspath
        self.client=gudev.Client('usb')
        self.int_udev=self.client.query_by_sysfs_path(sysfspath)
        self.int_entry=InterfaceEntry.InterfaceEntry(self.get_interface_name())

    def __str__(self):
        return self.get_formated_name()

    def get_udev_object(self):
        return self.int_udev
    
    def get_formated_name(self):
        inttype=self.int_udev.get_property('INTERFACETYPE')
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(inttype):
            print "The device type must be x-usb-device/'name_of_device'"
            sys.exit(1)

        inttype = inttype.split("/")[1].replace('-',' ').capitalize()
        return inttype

    def get_interface_name(self):
        inttype=self.int_udev.get_property('INTERFACETYPE')
        regexp = re.compile('x-usb-device/[a-z]+')
        if not regexp.match(inttype):
            print "The device type must be x-usb-device/'name_of_device'"
            sys.exit(1)

        return inttype.split("/")[1]

    def get_interface_type(self):
        inttype=self.int_udev.get_property('INTERFACETYPE')
        return inttype

    def get_interface_entry(self):
        return self.int_entry
