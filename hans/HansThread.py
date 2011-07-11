
import gtk
import threading
from . import (ActionSelectorSimple, ActionLauncher)
from model import (DeviceClass, InterfaceEntry)

class HansThread(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
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
            de.setInterface(selected_interface.get_name())
            de.setActions(';'.join(selected_actions))
            de.write()

        if isinstance(selected_interface, InterfaceEntry.InterfaceEntry):
            self.launch_actions(selected_interface, selected_actions)

    def launch_actions(self, interface_entry, action_list):

        launcher = ActionLauncher.ActionLauncher(interface_entry)
        launcher.execute(action_list)
