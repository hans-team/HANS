
import gobject
import gio
import gtk
import types
from hans import _
from hans.helpers import get_builder
from hans.model import InterfaceEntry

TREEVIEW_ICON_SIZE = 16

class ApplicationSelectorWindow(gtk.Window):

    __gtype_name__ = "ApplicationSelectorWindow"

    def __init__(self, interface=None, execute_callback=None):
        gtk.Window.__init__(self)

    def main(self):
        gtk.main()

    def __new__(cls, interface=None, execute_callback=None):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        """
        builder = get_builder('ApplicationSelectorWindow')
        new_object = builder.get_object('applicationselector_window')
        new_object.finish_initializing(builder, interface, execute_callback)
        return new_object

    def finish_initializing(self, builder, interface, execute_callback):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ActionSelectorDialog object with it in order to
        finish initializing the start of the new ActionSelectorDialog
        instance.
        """

        self.treeviewApplications = builder.get_object('treeviewApplications')
        self.lblDescription = builder.get_object('lblDescription')
        self.chkDefaultApplication = builder.get_object('chkDefaultApplication')
        self.btnSelect = builder.get_object('btnSelect')
        self.btnCancel = builder.get_object('btnCancel')

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.interface = interface

        self.interfacetype = self.interface.get_interface_class().get_interface_type()
        self.default_app = gio.app_info_get_default_for_type(self.interfacetype, True)
        self.added_applications = []
        self.selected_app = None

        self.builder.connect_signals(self)
        if type(execute_callback) == types.FunctionType or type(execute_callback) == types.MethodType:
            self.connect('execute-application', execute_callback)

        self._translate()
        self._init_treeview()
        self._load_applications()
        self.show()

    def _translate(self):
        description = _('Select an application to open')
        description = '<b>%s &lt;&lt;%s&gt;&gt;</b>' % (description, self.interfacetype)
        self.set_title(_('Application selector'))
        self.lblDescription.set_markup(description)
        self.chkDefaultApplication.set_label(_('Check as default application for that interface type') + '.')
        self.btnSelect.set_label(_('Select'))
        self.btnCancel.set_label(_('Cancel'))

    def get_is_default_application(self):
        return self.chkDefaultApplication.get_active()

    def on_deleteEvent(self, widget, data=None):
        gtk.main_quit()

    def on_btnSelectClicked(self, button):
        selection = self.treeviewApplications.get_selection()
        (model, iter) = selection.get_selected()
        if iter == None:
            return
        path = model.get_path(iter)
        self.selected_app = model.get_value(iter, 0)
        self.emit_execute_action(path, self.selected_app)

    def on_btnCancelClicked(self, button):
        self.destroy()

    def on_treeviewApplicationsRowActivated(self, treeview, path, user_param1):
        model = treeview.get_model()
        iter = model.get_iter(path)
        self.selected_app = model.get_value(iter, 0)
        self.emit_execute_action(path, self.selected_app)

    def emit_execute_action(self, path, app_info):

        if isinstance(app_info, HeaderAppInfo):
            if self.treeviewApplications.row_expanded(path):
                self.treeviewApplications.collapse_row(path)
            else:
                self.treeviewApplications.expand_row(path, False)

        else:
            self.emit('execute-application', self.selected_app)
            self.destroy()

    def _init_treeview(self):

        tvcolumn = gtk.TreeViewColumn(_('Applications'))

        cell = gtk.CellRendererPixbuf()
        tvcolumn.pack_start(cell, False)
        tvcolumn.set_cell_data_func(cell, self._render_column_pixbuf)

        cell = gtk.CellRendererText()
        #tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.set_cell_data_func(cell, self._render_column_text)

        self.treeviewApplications.append_column(tvcolumn)
        self.treeviewApplications.set_enable_search(True)
        self.treeviewApplications.set_search_column(0)
        self.treeviewApplications.set_show_expanders(True)

        treestore = gtk.TreeStore(object)
        self.treeviewApplications.set_model(treestore)

    def _load_applications(self):

        treestore = self.treeviewApplications.get_model()
        treestore.clear()

        self.added_applications = []

        #self.interfacetype = 'text/xml'

        app_list = gio.app_info_get_default_for_type(self.interfacetype, False)
        row = self._load_application_group(_('Default application'), '', [app_list], treestore)

        app_list = gio.app_info_get_all_for_type(self.interfacetype)
        self._load_application_group(_('Recommended applications'), '', app_list, treestore)

        app_list = gio.app_info_get_all()
        self._load_application_group(_('Other applications'), '', app_list, treestore)

        self.treeviewApplications.set_model(treestore)
        #self.treeviewApplications.expand_all()

        try:
            self.treeviewApplications.expand_row((0,), False)
        except:
            pass

    def _load_application_group(self, name, description, app_list, treestore):

        row = None
        app_list = self._filter_application_list(app_list)

        if len(app_list) > 0:
            dapp = HeaderAppInfo(name, description)
            row = treestore.append(None, [dapp])
            self._load_application_list(row, app_list, treestore)

        return row

    def _load_application_list(self, parent, app_list, treestore):

        for app_info in app_list:
            if not app_info in self.added_applications:
                treestore.append(parent, [app_info])
                self.added_applications.append(app_info)

    def _filter_application_list(self, app_list):
        _list = []
        for app_info in app_list:
            if isinstance(app_info, gio.AppInfo) and not app_info in self.added_applications and app_info.should_show():
                _list.append(app_info)
        return _list

    def _render_column_pixbuf(self, column, cell, model, iter):

        app_info = model.get_value(iter, 0)
        default_theme = gtk.icon_theme_get_default()

        try:
            gicon = app_info.get_icon()
            icon_info = default_theme.choose_icon(gicon.get_names(), TREEVIEW_ICON_SIZE, 0)
            pixbuf = icon_info.load_icon()

        except Exception:
            pixbuf = None

        cell.set_property('pixbuf', pixbuf)

    def _render_column_text(self, column, cell, model, iter):

        app_info = model.get_value(iter, 0)

        if isinstance(app_info, HeaderAppInfo):
            property = 'markup'
            text = '<b>%s</b>' % (app_info.get_name(),)
        else:
            property = 'text'
            text = app_info.get_name()

        cell.set_property(property, text)

class HeaderAppInfo():

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_icon(self):
        return None


gobject.type_register(ApplicationSelectorWindow)
gobject.signal_new(
    'execute-application', ApplicationSelectorWindow,
    gobject.SIGNAL_ACTION, gobject.TYPE_NONE,
    (object,)
)
