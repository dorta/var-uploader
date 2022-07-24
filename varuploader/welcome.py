# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import gi
gi.require_version('Gtk',  "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Box):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        self.add(main_box)

        box = Gtk.Box()
        main_box.pack_start(box, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(hbox, True, True, 0)

        box = Gtk.Box()
        hbox.pack_start(box, True, True, 0)

        box = Gtk.Box()
        hbox.pack_start(box, True, True, 0)

        new_release_button = Gtk.Button.new_with_label(f"Create New Release")
        new_release_button.connect("clicked", self.on_new_release_clicked)
        box.pack_start(new_release_button, True, True, 0)

        box = Gtk.Box()
        hbox.pack_start(box, True, True, 0)

        box = Gtk.Box()
        main_box.pack_start(box, True, True, 0)

    def on_new_release_clicked(self, button):
        self._parent.new_release_window.show_all()
        self.hide()
