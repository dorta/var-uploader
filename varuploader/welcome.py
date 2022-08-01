# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import gi
gi.require_version('Gtk',  "3.0")
from gi.repository import Gtk

from release import NewReleaseWindow


class MainWindow(Gtk.Box):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._image = None

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        self.add(main_box)

        box = Gtk.Box()
        main_box.pack_start(box, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_left(100)
        vbox.set_margin_right(100)

        label = Gtk.Label()
        label.set_text("Recovery SD card")
        vbox.pack_start(label, False, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Select a Recovery SD card...")
        self.entry.set_editable(False)
        vbox.pack_start(self.entry, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        open_file_button = Gtk.Button.new_with_label("Open")
        open_file_button.connect("clicked", self.on_open_clicked, self._parent)
        hbox.pack_start(open_file_button, True, True, 0)

        self.new_release_button = Gtk.Button.new_with_label("Create New Release")
        self.new_release_button.connect("clicked", self.on_new_release_clicked)
        self.new_release_button.set_sensitive(False)
        hbox.pack_start(self.new_release_button, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)
        main_box.pack_start(vbox, False, True, 0)

        box = Gtk.Box()
        main_box.pack_start(box, True, True, 0)

    def on_open_clicked(self, button, parent):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=parent,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            image = dialog.get_filename()
            self._image = image
            self.entry.set_text(image)
            self.new_release_button.set_sensitive(True)
            parent.con.remove(parent.new_release_window)
            parent.new_release_window = NewReleaseWindow(parent, image)
            parent.con.add(parent.new_release_window)
            parent.con.show()
            parent.show()

        dialog.destroy()

    def on_new_release_clicked(self, button):
        self._parent.new_release_window.show_all()
        self.hide()
