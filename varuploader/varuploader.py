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

from config import *
from release import NewReleaseWindow
from welcome import MainWindow


class VarUploaderGUI(Gtk.Window):
    def __init__(self):
        super(VarUploaderGUI, self).__init__(title=WINDOW_T)
        self.set_default_size(WINDOW_W, WINDOW_H)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.con = Gtk.Box()
        self.add(self.con)

        self.main_window = MainWindow(self)
        self.new_release_window = NewReleaseWindow(self)

        self.con.add(self.main_window)
        self.con.add(self.new_release_window)
        self.con.show()


def main():
    app = VarUploaderGUI()
    app.connect('delete-event', Gtk.main_quit)
    app.show()
    app.main_window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
