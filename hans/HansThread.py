
import gtk
import time
import threading
from . import (ActionSelectorSimple, ActionLauncher)
from model import (DeviceClass, InterfaceEntry)
from utils import notify

class HansThread():#threading.Thread):

    def __init__(self, device):
#        threading.Thread.__init__(self)
        self.device = device

    def run(self):

        notify("HANS - New "+ self.device.get_device_type() +" connected", self.device.get_formated_name(), self.device.get_pixbuf())

        #defaults = self.device.get_defaults_entry()
        #action_list = defaults.get_actions()
        action_list=list()

        if len(action_list) != 0:
            interface_filename = defaults.get_interface()
            interface_entry = InterfaceEntry.InterfaceEntry(interface_filename)
            action_list = action_list.split(';')
            self.launch_actions(interface_entry, action_list)

        else:
            dialog = ActionSelectorSimple.ActionSelectorSimple(self.device, self.on_actionExecuted)
            dialog.main()

    def on_actionExecuted(self, button, dialog):

        selected_interface = dialog.get_selected_interface()
        selected_actions = dialog.get_selected_actions()
        set_as_default = dialog.get_set_as_default()
        #dialog.destroy()

        print '--------------------'
        print selected_interface
        print selected_actions
        print set_as_default
        print '--------------------'

        if set_as_default:
            de = dialog.device.get_defaults_entry()
            de.set_interface(selected_interface.get_name())
            de.set_actions(';'.join(selected_actions))
            de.write()

        if isinstance(selected_interface, InterfaceEntry.InterfaceEntry):
            self.launch_actions(selected_interface, selected_actions)

    def launch_actions(self, interface_entry, action_list):
        launcher = ActionLauncher.ActionLauncher(interface_entry)
        launcher.execute(action_list)
