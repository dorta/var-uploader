# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import gi
gi.require_version('Gtk',  "3.0")
from gi.repository import Gtk

from utils import calculate_sha224_hash
from utils import get_current_date, get_file_size
import yaml


class NewReleaseWindow(Gtk.Box):
    def __init__(self, parent, file_path=None):
        super().__init__()
        self._parent = parent
        self._date = get_current_date("%m/%d/%Y")
        self._file_path = file_path
        self._file_sha224 = None if not file_path else calculate_sha224_hash(file_path)
        self._file_size = None if not file_path else get_file_size(file_path)
        self._info = {"Version": None, "Date": self._date, "Yocto": None,
                      "Android": None, "Path": None,
                      "SHA224": self._file_sha224, "Size": self._file_size}

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        main_box.set_margin_left(20)
        main_box.set_margin_right(20)
        self.add(main_box)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.on_back_clicked)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)

        self.release_page = ReleasePage(self._info)
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

        return {'Release': self.release_page.release_dict,
                'Changes': self.changelog_page.changelog_dict,
                'Sources': self.sources_page.sources_dict}

    def on_back_clicked(self, button):
        self._parent.main_window.show_all()
        self.hide()

    def on_export_release_clicked(self, button):
        yaml_dict = self._export_yml()

        confirmation_dialog = ConfirmationDialog(self._parent, yaml_dict)
        confirmation_response = confirmation_dialog.run()

        if confirmation_response == Gtk.ResponseType.OK:
            login_dialog = LoginDialog(confirmation_dialog)
            login_response = login_dialog.run()

            if login_response == Gtk.ResponseType.OK:
                """
                    TODO: Validate FTP credentials and upload Recovery SD card + changelog file
                """

                with open('release_changelog.yaml', 'a') as f:
                    yaml.dump(yaml_dict, f,  Dumper=IndentDumper, default_flow_style=False,
                            explicit_start=True, sort_keys=False)
            else:
                """ TODO """

            login_dialog.destroy()
        confirmation_dialog.destroy()


class ConfirmationDialog(Gtk.Dialog):
    def __init__(self, parent, yaml_dict):
        super().__init__(title="Release Changelog Preview", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)

        window_size = parent.get_size()
        self.set_default_size(*window_size)

        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        label_box = Gtk.Box()

        label = Gtk.Label(label=yaml.dump(yaml_dict, Dumper=IndentDumper, sort_keys=False).replace("  ", "\t"))
        label_box.pack_start(label, False, True, 10)
        sw.add(label_box)

        box = self.get_content_area()
        box.add(sw)
        self.show_all()


class LoginDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Login", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(480, 320)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)
        vbox.set_margin_top(10)

        label = Gtk.Label(label="Enter FTP credentials")
        vbox.pack_start(label, False, True, 0)

        username_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        username_label =  Gtk.Label(label="Username:\t")
        username_entry = Gtk.Entry()
        username_entry.set_visibility(False)
        username_hbox.pack_start(username_label, False, True, 0)
        username_hbox.pack_start(username_entry, True, True, 0)
        vbox.pack_start(username_hbox, False, True, 0)

        passwd_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        passwd_label =  Gtk.Label(label="Password:\t")
        passwd_entry = Gtk.Entry()
        passwd_entry.set_visibility(False)
        passwd_hbox.pack_start(passwd_label, False, True, 0)
        passwd_hbox.pack_start(passwd_entry, True, True, 0)
        vbox.pack_start(passwd_hbox, False, True, 0)

        box = self.get_content_area()
        box.add(vbox)
        self.show_all()


class ReleasePage(Gtk.Box):
    def __init__(self, release_info):
        super().__init__()
        self._release_info = release_info
        self.release_entries = []
        self.release_dict = {}

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)
        vbox.set_margin_top(5)
        self.add(vbox)

        for info in self._release_info:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            label = Gtk.Label(label=f"{info:>12}\t")
            entry = Gtk.Entry()
            if self._release_info[info]:
                entry.set_text(self._release_info[info])
                entry.set_editable(False)
            else:
                entry.set_placeholder_text(f"Add {info.lower()}...")
            self.release_entries.append(entry)
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(entry, True, True, 0)
            vbox.pack_start(hbox, False, True, 0)

    def write_release_entries(self):
        for info, entry in zip(self._release_info, self.release_entries):
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
            self.main_box.set_margin_left(10)
            self.main_box.set_margin_right(10)
            self.main_box.set_margin_top(5)
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
            entry.set_placeholder_text("Add changelog...")
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
            self.main_box.set_margin_left(10)
            self.main_box.set_margin_right(10)
            self.main_box.set_margin_top(5)
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
            entry.set_placeholder_text(f"Add {subsection.lower()}...")
            self.repo_entries[target][subsection] = entry
            source_hbox.pack_start(label, False, False, 0)
            source_hbox.pack_start(entry, True, True, 0)
            source_vbox.pack_start(source_hbox, False, True, 0)

        def write_repo_entries(self):
            for target in self.repo_entries:
                for subsection in self.repo_entries[target]:
                    self.repo_dict[target][subsection] = self.repo_entries[target][subsection].get_text()

            return self.repo_dict


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def add_notebook_page(notebook, page_object, page_name):
    page = page_object
    notebook.append_page(page)
    notebook.set_tab_label_text(page, page_name)
