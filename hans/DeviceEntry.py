import os.path
from hans import DeviceClassDB


class DeviceClass():


    def __init__(self, sysfspath):
        self.sysfspath(sysfspath)
        self.checkKnowDeviceClass(sysfspath)
        

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
