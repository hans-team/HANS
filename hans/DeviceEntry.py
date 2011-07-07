
import InterfaceEntry
import DefaultsEntry
import os

class DeviceEntry:

    def __init__(self, device_name):
        self.device_name = device_name
        self.de_path = '/home/ahernandez/dev/HANS/db/%s.default' % (device_name,)
        self.de = None

    def getName(self):
        return self.device_name

    def get_interfaces(self):
        list = []
        list.append(InterfaceEntry.InterfaceEntry('/home/ahernandez/dev/HANS/db/ebook.interface'))
        list.append(InterfaceEntry.InterfaceEntry('/home/ahernandez/dev/HANS/db/mobile.interface'))
        return list

    def get_defaults_entry(self):

        if isinstance(self.de, DefaultsEntry.DefaultsEntry):
            return self.de

        if os.path.exists(self.de_path):
            self.de = DefaultsEntry.DefaultsEntry(self.de_path)
            return self.de

        fp = open(self.de_path, 'w')
        fp.write('[Defaults Entry]')
        fp.close()
        self.de = DefaultsEntry.DefaultsEntry(self.de_path)
        return self.de
