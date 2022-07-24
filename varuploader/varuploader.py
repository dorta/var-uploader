#!/usr/bin/env python3

# Copyright 2022 Variscite LTD
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys

from args import args_parser
from config import *
from release import NewReleaseWindow
from utils import calculate_sha224_hash
from utils import get_current_date, get_file_size
from welcome import MainWindow


class VarUploaderGUI(Gtk.Window):
    def __init__(self):
        super(VarUploaderGUI, self).__init__(title=WINDOW_T)
        self.set_default_size(WINDOW_W, WINDOW_H)
        self.set_position(Gtk.WindowPosition.CENTER)

        container = Gtk.Box()
        self.add(container)

        self.main_window = MainWindow(self)
        self.new_release_window = NewReleaseWindow(self)

        container.add(self.main_window)
        container.add(self.new_release_window)
        container.show()


def main():
    parser, args = args_parser()
    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    changelog_file_name = MX8_YAML_CHANGELOG_FILES[args.som]
    size = get_file_size(args.image)
    sha224_hash = calculate_sha224_hash(args.image)

    sys.stdout.write("Starting User Interface\n")
    start_ui()

def start_ui():
    app = VarUploaderGUI()
    app.connect('delete-event', Gtk.main_quit)
    app.show()
    app.main_window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
