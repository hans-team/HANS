import pynotify


from hans.hansconfig import get_data_path
import gettext
import os
import gtk
import sys
from gettext import gettext as _
gettext.textdomain('hans')


def notify(title, message, icon, timeout=None):
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
    if not timeout == None:
        notify.set_timeout(timeout)
    if not notify.show():
        print "Failed to send notification"

def get_defaults_path():
    return os.path.join(os.path.expanduser('~'), "hans/defaults")

def get_actions_path():
    return os.path.join(get_data_path, "db/actions")

def get_interfaces_path():
    return os.path.join(get_data_path, "db")

def get_pixbuf_from_file(self, file_name, icon_size, flags=gtk.gdk.INTERP_BILINEAR):
    if not os.path.exists(file_name):
        return None
    image = gtk.Image()
    image.set_from_file(file_name)
    pixbuf = image.get_pixbuf()
    pixbuf = pixbuf.scale_simple(icon_size, icon_size, flags)
    return pixbuf

def get_theme_icon_path(self, icon_name, icon_size, flags=0):
    icon_theme = gtk.icon_theme_get_default()
    icons = icon_theme.list_icons()
    if not icon_name in icons:
        return None
    file_name = icon_theme.lookup_icon(icon_name, icon_size, flags).get_filename()
    return file_name
