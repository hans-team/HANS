import os.path
import gudev
import gettext
import InterfaceClass
import DefaultsEntry
from hans import utils
from hans.hansconfig import get_data_path
from gettext import gettext as _
gettext.textdomain('hans')

class DeviceClass():


    def __init__(self, sysfspath):
        self.sysfspath = sysfspath
        self.client = gudev.Client('usb')
        self.dev_udev = self.client.query_by_sysfs_path(sysfspath)
        if self.dev_udev == None:
            raise Exception('Device not found: ' + sysfspath)
        self.de = None
        self.list_interfaces = None

    def __str__(self):
        return self.getFormatedName()

    def get_sysfs_path(self):
        return self.sysfspath

    def get_udev_object(self):
        return self.dev_udev

    def get_formated_name(self):
        vendor = self.dev_udev.get_property('ID_VENDOR')
        model = self.dev_udev.get_property('ID_MODEL')
        vendor = vendor.replace('_', ' ')
        model = model.replace('_', ' ')
        return vendor + " " + model

    def get_vendor(self):
        vendor = self.dev_udev.get_property('ID_VENDOR')
        vendor = vendor.replace('_', ' ')
        return vendor

    def get_model(self):
        model = self.dev_udev.get_property('ID_MODEL')
        model = model.replace('_', ' ')
        return model

    def get_interfaces(self):
        if self.list_interfaces == None:
            self.list_interfaces = list()
            l_usb_udev = self.client.query_by_subsystem('usb')
            for usb_udev in l_usb_udev:
                if self.sysfspath + "/" in usb_udev.get_sysfs_path():
                   interface_udev = InterfaceClass.InterfaceClass(usb_udev.get_sysfs_path())
                   self.list_interfaces.append(interface_udev)

            return self.list_interfaces
        else:
            return self.list_interfaces

    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flag=0):
        if self.dev_udev.get_property('ICON'):
            filename=self.dev_udev.get_property('ICON')
            if not os.path.exists(filename):
                filename = utils.get_theme_icon_path(filename, icon_size, flag)
                return filename
            return filename
        num_interfaces=self.get_number_interfaces()
        if num_interfaces == 1:
            return self.get_interfaces()[0].get_interface_entry().get_icon(icon_size, flag)
        else:
            return utils.get_default_icon_device()
                                         
    def get_pixbuf(self, icon_size=utils.DEFAULT_ICON_SIZE, flag=0):
        return utils.get_pixbuf_from_file(self.get_icon(), icon_size, flag)

    def get_number_interfaces(self):
        if self.list_interfaces == None:
            self.list_interfaces = self.get_interfaces()
        return len(self.list_interfaces)

    def get_defaults_entry(self):

        filename_default = self.get_vendor() + "-" + self.get_model()
        filename_default = filename_default.replace(' ', '_')
        filename_default += '.defaults'

        if isinstance(self.de, DefaultsEntry.DefaultsEntry):
            return self.de

        if os.path.exists(os.path.join(utils.get_defaults_path(), filename_default)):
            self.de = DefaultsEntry.DefaultsEntry(filename_default)
            return self.de

        if not os.path.exists(utils.get_defaults_path()):
            os.makedirs(utils.get_defaults_path(), 0775)

        fp = open(os.path.join(utils.get_defaults_path(), filename_default), 'w')
        fp.write('[Defaults Entry]')
        fp.close()
        self.de = DefaultsEntry.DefaultsEntry(filename_default)
        return self.de

    def get_device_type(self):
        num_interfaces=self.get_number_interfaces()
        if self.dev_udev.get_property('ICON'):
            filename=self.dev_udev.get_property('ICON')
            if filename=='camera-photo':
                return _("camera photo")
            elif filename=='multimedia-player':
                return _("multimedia player")
            else:
                return filename
        else:  
            if num_interfaces == 1:
                return self.get_interfaces()[0].get_formated_name()
            else:
                return _("device")

                
