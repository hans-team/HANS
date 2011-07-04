

import os

import ActionSelectorDialog
from . import (DeviceEntry, InterfaceEntry)
from actions import *

class ActionLauncher:

    def __init__(self, udev_item):
        self._udev_item = udev_item
        self._action_list = udev_item.get_actions()
        self._non_interactive_actions = {}

        for action_name in self._action_list:
            action = self._action_list[action_name]
            if not action.getInteractive():
                self._non_interactive_actions[action.getName()] = action

    def show_selector_dialog(self):
        dialog = ActionSelectorDialog.ActionSelectorDialog(self._udev_item)
        dialog._btnExec.connect('clicked', self.on_btnExecClicked, dialog)
        dialog._treeviewActions.connect('row-activated', self.on_treeviewActionsRowActivated, dialog)
        ret = dialog.run()
        dialog.destroy()

    def execute(self, action_list):

        for action_name in action_list:

            if not action_name in self._action_list:
                continue

            action_entry = self._action_list[action_name]
            action_instance = self._get_action_instance(action_entry)

            if action_instance != None:
                action_instance.execute(self._udev_item)

    def execute_non_interactive(self):
        self.execute(self._non_interactive_actions)

    def _get_action_instance(self, action):

        try:
            action_name = action.getName() + 'Action'
            action_module = globals()[action_name]
        except KeyError, e:
            action_name = 'DefaultAction'
            action_module = globals()[action_name]

        a = action_module.get_instance(action)
        return a

    def on_btnExecClicked(self, button, dialog):
        selected_actions = dialog.get_selected_actions()
        self.execute(selected_actions)

    def on_treeviewActionsRowActivated(self, treeview, path, column, dialog):
        selected_actions = dialog.get_selected_actions()
        self.execute(selected_actions)
