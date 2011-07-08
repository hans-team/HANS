
from xdg.IniFile import *
import os
import types
from hans import utils

class DefaultsEntry(IniFile):

    defaultGroup = 'Defaults Entry'

    def __init__(self, filename=None):
        print 'init'
        self.content = dict()
        self.parse(os.path.join(utils.getDefaultsPath(), filename))

    def __str__(self):
        return self.getName()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, file):
        IniFile.parse(self, file, [self.defaultGroup])

    def write(self):
        IniFile.write(self, self.filename)

    # start standard keys
    def getInterface(self):
        return self.get('Interface')
    def setInterface(self, interface):
        self.set('Interface', interface)

    def getActions(self):
        return self.get('Actions')
    def setActions(self, actions):
        self.set('Actions', actions)

    def new(self, filename):
        print 'new'
        self.content = dict()
        self.addGroup(self.defaultGroup)
        self.filename = os.path.join(utils.getDefaultsPath(), filename)
