# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from platform import release
import gi
gi.require_version('Gtk',  "3.0")
from gi.repository import Gtk

import yaml


class NewReleaseWindow(Gtk.Box):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        self.add(main_box)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.on_back_clicked)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)

        self.release_page = ReleasePage()
        self.changelog_page = ChangelogPage()
        self.sources_page = SourcesPage()

        add_notebook_page(notebook, self.release_page, "Release")
        add_notebook_page(notebook, self.changelog_page, "Changelog")
        add_notebook_page(notebook, self.sources_page, "Sources")

        export_release_button = Gtk.Button.new_with_label("Export Release")
        export_release_button.connect("clicked", self.on_export_release_clicked)

        main_box.pack_start(back_button, False, True, 5)
        main_box.pack_start(notebook, True, True, 5)
        main_box.pack_start(export_release_button, False, True, 5)

    def _export_yml(self):
        self.release_page.write_release_entries()
        self.changelog_page.write_changelog_entries()
        self.sources_page.write_sources_entries()

        yaml_dict = {'Release': self.release_page.release_dict,
                     'Changes': self.changelog_page.changelog_dict,
                     'Sources': self.sources_page.sources_dict}

        with open('release_changelog.yaml', 'a') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, explicit_start=True, sort_keys=False)

    def on_back_clicked(self, button):
        self._parent.main_window.show_all()
        self.hide()

    def on_export_release_clicked(self, button):
        self._export_yml()


class ReleasePage(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.release_info = ["Version", "Date", "Yocto", "Android", "Path", "SHA224", "Size"]
        self.release_entries = []
        self.release_dict = {}

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        self.add(vbox)

        for info in self.release_info:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            label = Gtk.Label(label=f"{info:>12}\t")
            entry = Gtk.Entry()
            entry.set_text(f"Add {info.lower()}...")
            self.release_entries.append(entry)
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(entry, True, True, 0)
            vbox.pack_start(hbox, False, True, 0)

    def write_release_entries(self):
        for info, entry in zip(self.release_info, self.release_entries):
            self.release_dict[info] = entry.get_text()


class ChangelogPage(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.changelog_dict = {}

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.add(notebook)

        self.yocto_page = self.UpdatesPage()
        self.android_page = self.UpdatesPage()

        add_notebook_page(notebook, self.yocto_page, "Yocto")
        add_notebook_page(notebook, self.android_page, "Android")

    def write_changelog_entries(self):
        self.changelog_dict["Yocto"] = self.yocto_page.write_updates_entries()
        self.changelog_dict["Android"] = self.android_page.write_updates_entries()

    class UpdatesPage(Gtk.Box):
        def __init__(self):
            super().__init__()
            self.updates_entries = {}
            self.updates_dict =  {}

            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.main_box.set_hexpand(True)
            self.main_box.set_vexpand(True)
            self.add(self.main_box)

            self.sw_vbox = []

            self.add_changelog_section("U-Boot", 0)
            self.add_changelog_section("Linux", 1)

        def add_changelog_section(self, target, pos):
            self.updates_entries[target] = []
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_hexpand(True)
            vbox.set_vexpand(True)

            header_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=f"{target} Changelog")
            add_button = Gtk.Button.new_with_label("Add New")
            add_button.connect("clicked", self.on_add_button_clicked, target, pos)
            header_hbox.pack_start(label, True, True, 0)
            header_hbox.pack_start(add_button, False, False, 0)
            vbox.pack_start(header_hbox, False, True, 0)

            sw = Gtk.ScrolledWindow()
            vbox.pack_start(sw, True, True, 0)
            sw_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            sw.add(sw_vbox)
            self.sw_vbox.append(sw_vbox)
            self.main_box.pack_start(vbox, True, True, 0)

        def write_updates_entries(self):
            for target, updates_list in self.updates_entries.items():
                self.updates_dict[target] = []

                for update in updates_list:
                    self.updates_dict[target].append(update.get_text())

                if not updates_list:
                    self.updates_dict[target] = ['No changes']

            return self.updates_dict

        def on_add_button_clicked(self, button, target, pos):
            sw_hbox =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            sw_hbox.set_margin_left(10)
            sw_hbox.set_margin_right(10)
            entry = Gtk.Entry()
            entry.set_text("Add changelog...")
            self.updates_entries[target].append(entry)
            rm_button = Gtk.Button.new_with_label("Remove")
            rm_button.connect("clicked", self.on_rm_button_clicked, sw_hbox, entry, target, pos)
            sw_hbox.pack_start(entry, True, True, 0)
            sw_hbox.pack_start(rm_button, False, False, 0)
            self.sw_vbox[pos].pack_start(sw_hbox, False, True, 0)
            self.show_all()

        def on_rm_button_clicked(self, button, widget, entry, target, pos):
            self.updates_entries[target].remove(entry)
            self.sw_vbox[pos].remove(widget)
            self.show_all()


class SourcesPage(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.sources_dict = {}

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.add(notebook)

        self.yocto_page = self.RepoPage("meta-variscite-imx")
        self.android_page = self.RepoPage("MX6x-Android")

        add_notebook_page(notebook, self.yocto_page, "Yocto")
        add_notebook_page(notebook, self.android_page, "Android")

    def write_sources_entries(self):
        self.sources_dict["Yocto"] = self.yocto_page.write_repo_entries()
        self.sources_dict["Android"] = self.android_page.write_repo_entries()

    class RepoPage(Gtk.Box):
        def __init__(self, meta):
            super().__init__()
            self.repo_entries = {}
            self.repo_dict = {}
            self._meta = meta

            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.main_box.set_hexpand(True)
            self.main_box.set_vexpand(True)
            self.add(self.main_box)

            self._add_source_section('U-Boot')
            self._add_source_section('Linux')
            self._add_source_section(self._meta)

        def _add_source_section(self, target):
            self.repo_entries[target] = {}
            self.repo_dict[target] = {}

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_hexpand(True)
            vbox.set_vexpand(True)

            label = Gtk.Label(label=f"{target} Source")
            vbox.pack_start(label, False, True, 0)

            source_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

            self._add_subsection('Git Repository', target, source_vbox)
            self._add_subsection('Git Branch', target, source_vbox)
            self._add_subsection('Git Commit ID', target, source_vbox)

            vbox.pack_start(source_vbox, True, True, 0)
            self.main_box.pack_start(vbox, True, True, 0)

        def _add_subsection(self, subsection, target, source_vbox):
            source_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=f"{subsection:>16}\t")
            entry = Gtk.Entry()
            entry.set_text(f"Add {subsection.lower()}...")
            self.repo_entries[target][subsection] = entry
            source_hbox.pack_start(label, False, False, 0)
            source_hbox.pack_start(entry, True, True, 0)
            source_vbox.pack_start(source_hbox, False, True, 0)

        def write_repo_entries(self):
            for target in self.repo_entries:
                for subsection in self.repo_entries[target]:
                    self.repo_dict[target][subsection] = self.repo_entries[target][subsection].get_text()

            return self.repo_dict


def add_notebook_page(notebook, page_object, page_name):
    page = page_object
    notebook.append_page(page)
    notebook.set_tab_label_text(page, page_name)
