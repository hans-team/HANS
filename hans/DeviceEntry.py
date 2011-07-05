
import InterfaceEntry

class DeviceEntry:
    def __init__(self):
        pass
    def get_interfaces(self):
        list = []
        list.append(InterfaceEntry.InterfaceEntry('/home/ahernandez/dev/HANS/db/ebook.interface'))
        list.append(InterfaceEntry.InterfaceEntry('/home/ahernandez/dev/HANS/db/mobile.interface'))
        return list
