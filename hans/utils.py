import pynotify

import gettext
from gettext import gettext as _
gettext.textdomain('hans')


def notify(device,  message):
    notify = pynotify.Notification("HANS notification - "+device, message)
    notify.set_urgency(pynotify.URGENCY_CRITICAL)
    notify.set_category("device")

    if not notify.show():
        print "Failed to send notification"

