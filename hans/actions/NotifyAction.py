

import os
import pynotify

def get_instance(action_entry):
    return NotifyAction(action_entry)

class NotifyAction():

    def __init__(self, action_entry):

        self._action_entry = action_entry

        if not pynotify.init("HANS notification"):
            sys.exit(1)

    def execute(self, udev_item):

        notify = pynotify.Notification("HANS notification - " + udev_item.getName(), udev_item.getNotify())
        #notify.set_urgency(pynotify.URGENCY_CRITICAL)
        notify.set_category("device")

        if not notify.show():
            print "Failed to send notification"

