
from actions import *

class ActionLauncher:

    def __init__(self, interface_entry):
        self._interface_entry = interface_entry
        self._action_list = interface_entry.get_actions()

    def execute(self, action_list):

        for action_name in action_list:

            if not action_name in self._action_list:
                continue

            try:
                action_entry = self._action_list[action_name]
                action_instance = self._get_action_instance(action_name, action_entry)
                print 'Instance for action "%s": ' % (action_name,), action_instance
                action_instance.execute(self._interface_entry)

            except Exception, e:
                print e

    def _get_action_instance(self, action_name, action_entry):

        try:
            action_name = action_name.capitalize() + 'Action'
            action_module = globals()[action_name]

        except KeyError, e:
            action_name = 'DefaultAction'
            action_module = globals()[action_name]

        action = None

        try:
            action = action_module.get_instance(action_entry)

        except Exception, e:
            raise e

        return action
