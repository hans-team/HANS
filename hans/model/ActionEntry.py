
from xdg.IniFile import *
import os
import types
from hans import utils
from hans.hansconfig import get_data_path

class ActionEntry(IniFile):

    default_group = 'Action Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(os.path.join(utils.get_actions_path(), filename))

    def __str__(self):
        return self.get_name()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, file):
        IniFile.parse(self, file, [self.default_group])

    # start standard keys
    def get_name(self):
        return self.get('Name')
    def set_name(self, name):
        self.set('Name', name)

    def get_comment(self):
        return self.get('Comment')
    def set_comment(self, comment):
        self.set('Comment', comment)

    def get_icon(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):

        filename = self.get('Icon')

        if not os.path.exists(filename):
            filename = utils.get_theme_icon_path(filename, icon_size, flags)

        if filename == None:
            filename = utils.get_default_icon_action()

        return filename

    def set_icon(self, icon):
        self.set('Icon', icon)

    def get_pixbuf(self, icon_size=utils.DEFAULT_ICON_SIZE, flags=0):
        filename = self.get_icon(icon_size, flags)
        pixbuf = utils.get_pixbuf_from_file(filename, icon_size)
        return pixbuf

    def get_exec(self):
        return self.get('Exec')
    def set_exec(self, s_exec):
        self.set('Exec', s_exec)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.default_group)
        self.filename = os.path.join(utils.get_actions_path(), filename)
