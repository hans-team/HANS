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
import os
import re
import utils
import ActionEntry

class InterfaceEntry(IniFile):
    "Class to parse and validate DesktopEntries"

    default_group = 'Interface Entry'

    def __init__(self, filename=None):
        self.content = dict()
        self.parse(os.path.join(utils.get_interfaces_path(),filename))

    def __str__(self):
        return self.get_name()

    def __cmp__(self, other):
        cmp2 = None
        if type(other) != types.NoneType:
            cmp2 = other.content
        return cmp(self.content, cmp2)

    def parse(self, file):
        IniFile.parse(self, file, ["Interface Entry"])

    def get_actions(self):

        selected_actions = self.get_action().split(';')
        action_path = utils.get_actions_path()
       # action_path = os.path.join(os.path.dirname(os.path.abspath(os.curdir)), 'db/actions')
        files = os.listdir(action_path)
        action_list = {}

        for filename in files:
            regexp = re.compile('^(.+)\.(action)$')
            m = regexp.match(filename)
            if m != None:
                groups = m.groups()
                action_name = groups[0]
                #file_path = os.path.join(action_path, filename)
                action_entry = ActionEntry.ActionEntry(filename)
                if action_name in selected_actions:
                    action_list[action_name] = action_entry

        return action_list

    # start standard keys
    def get_name(self):
        return self.get('Name')
    def set_name(self, name):
        self.set('Name', name)
    def get_notify(self):
        return self.get('Notify')
    def get_icon(self):
        return self.get('Icon')
    def set_icon(self, icon):
        self.set('Icon-Notify', icon)
    def get_action(self):
        return self.get('Action')
    def set_action(self, action):
        self.set('Action', action)
    def get_recommend_pkgs(self):
        return self.get('Recommend-Pkgs', locale=True)
    def set_recommend_pkgs(self, rpkgs):
        self.set('Recommend-Pkgs', rpkgs)

    def new(self, filename):
        self.content = dict()
        self.addGroup(self.default_group)
        self.filename = os.path.join(utils.get_interfaces_path(),filename)
