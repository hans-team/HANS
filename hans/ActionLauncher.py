

import os

import ActionSelectorDialog
from actions import *


class DeviceEntry:
    def __init__(self):
        pass

class ActionLauncher:

    def __init__(self, udev_item):
        self._udev_item = udev_item

    def show_selector_dialog(self):
        dialog = ActionSelectorDialog.ActionSelectorDialog(self._udev_item)
        ret = dialog.run()
        selected_action = dialog.get_actions()
        is_default_action = dialog.get_is_default_action()
        dialog.destroy()
        if ret == 1:
            # TODO: Do something with the get_is_default_action value
            self.execute(selected_action.getName())

    def execute(self, action_name):

        if isinstance(self._udev_item, DeviceEntry):
            action_name = 'Notify'
            action_entry = ActionEntry()
            action_entry.setName(action_name)

        elif isinstance(self._udev_item, InterfaceEntry):
            action_list = udev_item.get_actions()
            action_entry = action_list[action_name]

        action_instance = self._get_action_instance(action_entry)
        if action_instance != None:
            action_instance.execute()

    def _get_action_instance(self, action):
        try:
            action_name = action.getName() + 'Action'
            action_module = globals()[action_name]
        except KeyError, e:
            action_name = 'DefaultAction'
        action_module = globals()[action_name]
        a = action_module.get_instance(action)
        return a

def get_action_launcher(udev_item):
    launcher = ActionLauncher(udev_item)
    return launcher
