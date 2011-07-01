

import os
import dbus

def get_instance(action_entry):
    return NotifyAction(action_entry)

class NotifyAction():

    def __init__(self, action_entry):

        self._action_entry = action_entry

        item = ('org.freedesktop.Notifications')
        path = ('/org/freedesktop/Notifications')
        interface = ('org.freedesktop.Notifications')

        bus = dbus.SessionBus()
        notif = bus.get_object(item, path)
        self._notify_iface = dbus.Interface(notif, interface)

    def execute(self, udev_item):
        self.notify(udev_item)

    def notify(self, udev_item):

        # STRING    The optional name of the application sending the notification. Can be blank.
        app_name = udev_item.getName()

        # UINT32    The optional notification ID that this notification replaces.
        # The server must atomically (ie with no flicker or other visual cues) replace
        # the given notification with this one.
        # This allows clients to effectively modify the notification while it's active.
        # A value of value of 0 means that this notification won't replace any existing notifications.
        replaces_id = 0

        # STRING    The optional program icon of the calling application. See Icons. Can be an empty string, indicating no icon.
        app_icon = udev_item.getIcon_Notify()

        # STRING    The summary text briefly describing the notification.
        summary = udev_item.getName()

        # STRING    The optional detailed body text. Can be empty.
        body = udev_item.getNotify()

        # ARRAY    Actions are sent over as a list of pairs. Each even element in
        # the list (starting at index 0) represents the identifier for the action.
        # Each odd element in the list is the localized string that will be displayed to the user.
        actions = []

        # DICT    Optional hints that can be passed to the server from the client program.
        # Although clients and servers should never assume each other supports any specific hints,
        # they can be used to pass along information, such as the process PID or window ID,
        # that the server may be able to make use of. See Hints. Can be empty.
        hints = {}

        # INT32 The timeout time in milliseconds since the display of the notification
        # at which the notification should automatically close.
        # If -1, the notification's expiration time is dependent on the notification
        # server's settings, and may vary for the type of notification. If 0, never expire.
        expire_timeout = 10000

        self._notify_iface.Notify(app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout)
