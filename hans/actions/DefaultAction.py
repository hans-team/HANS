

import os, shlex, subprocess

def get_instance(action_entry):
    return DefaultAction(action_entry)

class DefaultAction():

    def __init__(self, action_entry):
        self._action_entry = action_entry

    def execute(self, udev_item):
#        cmd = self._action_entry.getExec()
#        args = [udev_item.getName()]
#        os.execv(cmd, args)

        cmd = self._action_entry.getExec() + ' "' + udev_item.getName() + '"'
        args = shlex.split(cmd)
        p = subprocess.Popen(args)
