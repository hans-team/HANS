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
import os.path


class DeviceEntry(IniFile):
    "Class to parse and validate DesktopEntries"

    defaultGroup = 'Device Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(filename)

    def __str__(self):
        return self.getName()

    def parse(self, file):
        IniFile.parse(self, file, ["Device Entry"])

    # start standard keys
    def getName(self):
        return self.get('Name')
    def setName(self, name):
        self.set('Name', name)
    def getNotify(self):
        return self.get('Notify')
    def setNotify(self, notify):
        self.set('Notify', notify)
    def getIcon_Notify(self):
        return self.get('Icon-Notify')
    def setIcon_Notify(self, icon_notify):
        self.set('Icon-Notify', icon_notify)
    def getAction(self):
        return self.get('Action')
    def setAction(self, action):
        self.set('Action', action)
    def getRecommend_Pkgs(self):
        return self.get('Recommend-Pkgs', locale=True)
    def setRecommend_Pkgs(self, rpkgs):
        self.set('Recommend-Pkgs', rpkgs)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.defaultGroup)
        self.filename = filename
