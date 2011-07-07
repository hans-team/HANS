
from xdg.IniFile import *
import os
import types
import utils
class ActionEntry(IniFile):

    default_group = 'Action Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(os.path.join(utils.get_actions_path(),filename))

    def __str__(self):
        return self.getName()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, file):
        IniFile.parse(self, file, [self.defaultGroup])

    # start standard keys
    def get_name(self):
        return self.get('Name')
    def set_name(self, name):
        self.set('Name', name)

    def get_comment(self):
        return self.get('Comment')
    def set_comment(self, comment):
        self.set('Comment', comment)

    def get_icon(self):
        return self.get('Icon')
    def set_icon(self, icon):
        self.set('Icon', icon)

    def get_exec(self):
        return self.get('Exec')
    def set_exec(self, s_exec):
        self.set('Exec', s_exec)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.default_group)
        self.filename = os.path.join(utils.get_actions_path(),filename)
