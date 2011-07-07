import pynotify


from hans.hansconfig import get_data_path
import gettext
import os
import gtk
import sys
from gettext import gettext as _
gettext.textdomain('hans')


def notify(title,  message, icon, timeout=None):
    if not pynotify.init("HANS Notifications"):
        sys.exit(1)
#    icon_notify=None
#    if icon==None:
#        icon_notify=gtk.gdk.pixbuf_new_from_file(os.path.join(get_data_path(),"media/default-icon-device.svg"))
#        #icon_notify=gtk.gdk.pixbuf_new_from_file('gnome-dev-removable-usb')
#    else:
#        self.icon_notify=gtk.gdk.pixbuf_new_from_file(icon)

    notify = pynotify.Notification(title, message)
    notify.set_icon_from_pixbuf(icon)
    notify.set_category("device")
    if not timeout==None:
        notify.set_timeout(timeout)
    if not notify.show():
        print "Failed to send notification"

def get_defaults_path():
    return os.path.join(os.path.expanduser('~'),"hans/defaults")

def get_actions_path():
    return os.path.join(get_data_path, "db/actions")

def get_interfaces_path():
    return os.path.join(get_data_path, "db")
