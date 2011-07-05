
from xdg.IniFile import *
import os.path
import types

class ActionEntry(IniFile):

    defaultGroup = 'Action Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(filename)

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
    def getName(self):
        return self.get('Name')
    def setName(self, name):
        self.set('Name', name)

    def getComment(self):
        return self.get('Comment')
    def setComment(self, comment):
        self.set('Comment', comment)

    def getIcon(self):
        return self.get('Icon')
    def setIcon(self, icon):
        self.set('Icon', icon)

    def getExec(self):
        return self.get('Exec')
    def setExec(self, s_exec):
        self.set('Exec', s_exec)

    def getInteractive(self):
        interactive = self.get('Interactive')
        if interactive.lower() == 'true' or (type(interactive) == int and interactive != 0):
            interactive = True
        else:
            interactive = False
        return interactive
    def setInteractive(self, interactive):
        if interactive.lower() == 'true' or (type(interactive) == int and interactive != 0):
            interactive = 'true'
        else:
            interactive = 'false'
        self.set('Interactive', interactive)

    def getMimetype(self):
        return self.get('MimeType')
    def setMimetype(self, mimetype):
        self.set('MimeType', mimetype)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.defaultGroup)
        self.filename = filename
