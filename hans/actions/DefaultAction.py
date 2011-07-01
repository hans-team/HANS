

import os
import shlex
import subprocess

def get_instance(action_entry):
    return DefaultAction(action_entry)

class DefaultAction():

    def __init__(self, action_entry):
        self._action_entry = action_entry

    def execute(self, udev_item):
        cmd = self._action_entry.getExec()
        args = shlex.split(cmd)
        p = subprocess.Popen(args)
