

import os

def get_instance(action_entry):
    return DefaultAction(action_entry)

class DefaultAction():

    def __init__(self, action_entry):
        self._action_entry = action_entry

    def execute(self):
        cmd = self._action_entry.getExec()
        args = [self._action_entry.getName(), self._action_entry.getComment()]
        os.execv(cmd, args)
