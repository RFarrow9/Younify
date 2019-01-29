import gi
#import youtube_converter
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

settings = Gtk.Settings.get_default()
settings.set_property("gtk-theme-name", "breeze-dark-red")
settings.set_property("gtk-application-prefer-dark-theme", True)  # if you want use dark theme, set second arg to True

# This file creates the GUI for the youtube-spotify interface
# Currently this all hangs off main, this needs changing in future
#
#
#
# TODO:
#   - Add tooltips (or explainy buttons) for what the settings actually do, these can be added without filling in (as we dont yet know)
#   - Work out what settings should exist
#   - Create array for holding 'songs' in Progress
#   - Add function for manually adding URLs (advanced tab?)
#   - Add button to 'show' the advanced tab
#   - Add function to manually parse URLs (using file import)
#   - This in theory could take in any file (html, csv etc) just by parsing out the youtube URLs?
#   - Make it so it actually sodding expands
#   - Make it so the 'In Progress' tab has an icon if files are being processed
#   - Hang everything off main _init_ call?
#   - Change the icon (make a custom one?)
#   - Need to be able to interact with processing array (delete, pause, prioritise?)
#   - Can this gui be launched from the plugin (from chrome/mozilla) - this might circumvent the need to develop for multiple environments
#   - How would this all be packaged?


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Youtube-Spotify Interface Settings")
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        #self.page1.add(Gtk.Label('Default Page!'))
        self.notebook.append_page(ListBox(6), Gtk.Label('Spotify Settings'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('This page should contain youtube settings (quality/logon) etc'))
        self.notebook.append_page(self.page2, Gtk.Label('Youtube Settings'))

        #ProgressBar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        Icon = Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        ProgressBar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label4 = Gtk.Label("File Progress")
        #ProgressBar.pack_start(label4, True, True, 0)
        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label('This page should contain the in progress files as they are downloaded/converted'))
        #self.page2.add(Gtk.Label('A page with an image for a Title.'))
        self.notebook.append_page(TreeViewFilter(),  Gtk.Label('In Progress')) #ProgressBar)


        #if 1 != 1:
        #   ProgressBar.pack_start(Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU), True, True, 0)

class ListBoxRowWithData(Gtk.ListBoxRow):

    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ListBox(Gtk.Box):

    def __init__(self, spacing):

        super(Gtk.Box, self).__init__()

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(box_outer)

        listbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        #listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        #row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        listbox.pack_start(hbox, True, True, 0)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        label1 = Gtk.Label("Local File Path")
    #    label2 = Gtk.Label("Requires internet access", xalign=0)
        vbox.pack_start(label1, True, True, 0)
    #    vbox.pack_start(label2, True, True, 0)


        vbox_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.entry = Gtk.Entry()
        self.entry.set_text("C:\Downloads")
        label1 = Gtk.Label("For example: C:\Downloads")
        label1.set_justify(Gtk.Justification.LEFT)
        vbox_1.pack_start(self.entry, True, True, 0)
        vbox_1.pack_start(label1, True, True, 0)
        hbox.pack_start(vbox_1, True, True, 0)

        #switch = Gtk.Switch()
        #switch.props.valign = Gtk.Align.CENTER
        #hbox.pack_end(switch, False, True, 0)
        #listbox.pack_start(hbox, True, True, 0)
        #listbox.add(row)

        #row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        listbox.pack_start(hbox, True, True, 0)
        label = Gtk.Label("Offline Mode", xalign=0)
        check = Gtk.CheckButton()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(check, False, True, 0)



        #row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        listbox.pack_start(hbox, True, True, 0)
        #row.add(hbox)
        label = Gtk.Label("Date Format", xalign=0)
        combo = Gtk.ComboBoxText()
        combo.insert(0, "0", "24-hour")
        combo.insert(1, "1", "AM/PM")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        #listbox.add(row)

        listbox_2 = Gtk.ListBox()
        items = 'Listbox functions, these output to console'.split()

        for item in items:
            listbox_2.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        listbox_2.set_sort_func(sort_func, None, False)
        listbox_2.set_filter_func(filter_func, None, False)

        def on_row_activated(listbox_widget, row):
            print(row.data)

        listbox_2.connect('row-activated', on_row_activated)

        box_outer.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()


        #list of tuples for each software, containing the software name, initial release, and main programming languages used
        #This shouldn't be a static list, but an iteration over an array
        #Static list as placeholder
software_list = [("Firefox", 2002,  "C++", 0.5),
                 ("Eclipse", 2004, "Java", 0.2 ),
                 ("Pitivi", 2004, "Python", 0.1),
                 ("Netbeans", 1996, "Java", 1.0),
                 ("Chrome", 2008, "C++", 0.0),
                 ("Filezilla", 2001, "C++", 0.3),
                 ("Bazaar", 2005, "Python", 0.4),
                 ("Git", 2005, "C", 0.9),
                 ("Linux Kernel", 1991, "C", 0.99),
                 ("GCC", 1987, "C", 0.0),
                 ("Frostwire", 2004, "Java", 0.0)]

class TreeViewFilter(Gtk.Box):

    def __init__(self):

        super(Gtk.Box, self).__init__()
        #Gtk.Window.__init__(self, title="Treeview Filter Demo")
        self.set_border_width(10)

        vbox_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #self.add(vbox)
        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)
        vbox_1.pack_start(vbox, True, True, 0)

        button = Gtk.CheckButton("Show text")
        button.connect("toggled", self.on_show_text_toggled)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.CheckButton("Activity mode")
        button.connect("toggled", self.on_activity_mode_toggled)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.CheckButton("Right to Left")
        button.connect("toggled", self.on_right_to_left_toggled)
        vbox.pack_start(button, True, True, 0)

        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)
        self.activity_mode = False

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        #self.add(self.grid)
        vbox_1.pack_start(self.grid, True, True, 0)
        self.add(vbox_1)


        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, int, str, float)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Software", "Release Year", "Programming Language", "Progress"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in ["Java", "C", "C++", "Python", "None", "CSS"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def on_show_text_toggled(self, button):
        show_text = button.get_active()
        if show_text:
            text = "some text"
        else:
            text = None
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)

    def on_activity_mode_toggled(self, button):
        self.activity_mode = button.get_active()
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)

    def on_right_to_left_toggled(self, button):
        value = button.get_active()
        self.progressbar.set_inverted(value)

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            new_value = self.progressbar.get_fraction() + 0.01

            if new_value > 1:
                new_value = 0

            self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
