
import gio
import DefaultAction
from .. import ApplicationSelectorWindow

def get_instance(action_entry):
    return OpenAction(action_entry)

class OpenAction(DefaultAction.DefaultAction):

    def execute(self, interface_entry):

        self.interface_entry = interface_entry

        mimetype = interface_entry.get_interface_class().get_interface_type()
        #mimetype = 'text/plain'
        app_info = gio.app_info_get_default_for_type(mimetype, True)

        if app_info == None or 1 == 1:
            self._open_dialog(interface_entry)

        else:
            self.on_actionExecuted(None, app_info)

    def _open_dialog(self, interface_entry):
        try:
            dialog = ApplicationSelectorWindow.ApplicationSelectorWindow(interface_entry, self.on_actionExecuted)
            dialog.main()

        except Exception:
            import traceback
            traceback.print_exc()

    def on_actionExecuted(self, dialog, app_info):
        # TODO: What are the parameters to be passed to the application?
        uris = []
        app_info.launch_uris(uris)
