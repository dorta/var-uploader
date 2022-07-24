# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import gi
gi.require_version('Gtk',  "3.0")
from gi.repository import Gtk


class NewReleaseWindow(Gtk.Box):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        self.add(main_box)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.on_back_clicked)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)

        release_page = ReleasePage()
        changelog_page = ChangelogPage()
        sources_page = SourcesPage()

        add_notebook_page(notebook, release_page, "Release")
        add_notebook_page(notebook, changelog_page, "Changelog")
        add_notebook_page(notebook, sources_page, "Sources")

        export_release_button = Gtk.Button.new_with_label("Export Release")
        export_release_button.connect("clicked", self.on_export_release_clicked)

        main_box.pack_start(back_button, False, True, 0)
        main_box.pack_start(notebook, True, True, 0)
        main_box.pack_start(export_release_button, False, True, 0)

    def on_back_clicked(self, button):
        self._parent.main_window.show_all()
        self.hide()

    def on_export_release_clicked(self, button):
        """
            TODO
        """
        print("Exporting Release...")


class ReleasePage(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.release_info = ["Version", "Date", "Yocto", "Android", "Path", "SHA224", "Size"]

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        self.add(vbox)

        for info in self.release_info:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            label = Gtk.Label(label=f"{info:>12}\t")
            entry = Gtk.Entry()
            entry.set_text(f"Add {info.lower()}...")
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(entry, True, True, 0)
            vbox.pack_start(hbox, False, True, 0)


class ChangelogPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.add(notebook)

        yocto_page = self.SubPage()
        android_page = self.SubPage()

        add_notebook_page(notebook, yocto_page, "Yocto")
        add_notebook_page(notebook, android_page, "Android")

    class SubPage(Gtk.Box):
        def __init__(self):
            super().__init__()

            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.main_box.set_hexpand(True)
            self.main_box.set_vexpand(True)
            self.add(self.main_box)

            self.sw_vbox = []

            self.add_changelog_section("U-Boot", 0)
            self.add_changelog_section("Linux", 1)

        def add_changelog_section(self, target, pos):
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_hexpand(True)
            vbox.set_vexpand(True)

            header_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=f"{target} Changelog")
            add_button = Gtk.Button.new_with_label("Add New")
            add_button.connect("clicked", self.on_add_button_clicked, pos)
            header_hbox.pack_start(label, True, True, 0)
            header_hbox.pack_start(add_button, False, False, 0)
            vbox.pack_start(header_hbox, False, True, 0)

            sw = Gtk.ScrolledWindow()
            vbox.pack_start(sw, True, True, 0)
            sw_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            sw.add(sw_vbox)
            self.sw_vbox.append(sw_vbox)
            self.main_box.pack_start(vbox, True, True, 0)

        def on_add_button_clicked(self, button, pos):
            sw_hbox =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            entry = Gtk.Entry()
            entry.set_text("Add changelog...")
            rm_button = Gtk.Button.new_with_label("Remove")
            rm_button.connect("clicked", self.on_rm_button_clicked, sw_hbox, pos)
            sw_hbox.pack_start(entry, True, True, 0)
            sw_hbox.pack_start(rm_button, False, False, 0)
            self.sw_vbox[pos].pack_start(sw_hbox, False, True, 0)
            self.show_all()

        def on_rm_button_clicked(self, button, widget, pos):
            self.sw_vbox[pos].remove(widget)
            self.show_all()


class SourcesPage(Gtk.Box):
    def __init__(self):
        super().__init__()

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.add(notebook)

        yocto_page = self.SubPage("meta-variscite-imx")
        android_page = self.SubPage("MX6x-Android")

        add_notebook_page(notebook, yocto_page, "Yocto")
        add_notebook_page(notebook, android_page, "Android")

    class SubPage(Gtk.Box):
        def __init__(self, meta):
            super().__init__()
            self._meta = meta

            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.main_box.set_hexpand(True)
            self.main_box.set_vexpand(True)
            self.add(self.main_box)

            self._add_source_section('U-Boot')
            self._add_source_section('Linux')
            self._add_source_section(self._meta)

        def _add_source_section(self, target):
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_hexpand(True)
            vbox.set_vexpand(True)

            label = Gtk.Label(label=f"{target} Source")
            vbox.pack_start(label, False, True, 0)

            source_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

            self._add_subsection('Git Repository', source_vbox)
            self._add_subsection('Git Branch', source_vbox)
            self._add_subsection('Git Commit ID', source_vbox)

            vbox.pack_start(source_vbox, True, True, 0)
            self.main_box.pack_start(vbox, True, True, 0)

        def _add_subsection(self,subsection, source_vbox):
            source_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=f"{subsection:>16}\t")
            entry = Gtk.Entry()
            entry.set_text(f"Add {subsection.lower()}...")
            source_hbox.pack_start(label, False, False, 0)
            source_hbox.pack_start(entry, True, True, 0)
            source_vbox.pack_start(source_hbox, False, True, 0)


def add_notebook_page(notebook, page_object, page_name):
    page = page_object
    notebook.append_page(page)
    notebook.set_tab_label_text(page, page_name)
