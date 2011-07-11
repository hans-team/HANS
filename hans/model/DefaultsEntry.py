
from xdg.IniFile import *
import os
import types
from hans import utils

class DefaultsEntry(IniFile):

    defaultGroup = 'Defaults Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(os.path.join(utils.get_defaults_path(), filename))

    def __str__(self):
        return self.get_name()

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
    def get_interface(self):
        return self.get('Interface')
    def set_interface(self, interface):
        self.set('Interface', interface)

    def get_actions(self):
        return self.get('Actions')
    def set_actions(self, actions):
        self.set('Actions', actions)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.defaultGroup)
        self.filename = os.path.join(utils.get_defaults_path(), filename)
