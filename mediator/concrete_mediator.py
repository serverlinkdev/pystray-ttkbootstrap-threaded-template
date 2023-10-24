"""
pystray-ttkbootstrap-threaded-template:
    A program to demonstrate use of pystray and ttkbootstrap using threads,
    using the Mediator design pattern.

    Copyright (C) 2023 serverlinkdev@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
from main_window import MainWindow
from mediator import Mediator
from systray import Systray


class ConcreteMediator(Mediator):
    """
    A class which implements the Mediator pattern.

    User's of this class should only:
    - Instantiate
    - Set mediator
    - Call in to this class using 'notify' method.
    """

    _main_window = None
    _systray = None

    def __init__(self):
        super().__init__()

    def notify(self, sender, event):

        # Handle the notify calls from main.py
        if sender == "Main":
            if event == "START":
                self._start_systray()
                self._start_main_window()

        # Handle the notify calls from Systray
        if isinstance(sender, Systray):
            self._main_window.notify("ConcreteMediator", event)

    def _start_systray(self):
        """
        Starts the Systray class.
        """
        self._systray = Systray()
        self._systray.mediator = self
        self._systray.notify("ConcreteMediator", "START")

    def _start_main_window(self):
        """
        Starts the MainWindow class
        """
        self._main_window = MainWindow()
        self._main_window.mediator = self
        self._main_window.notify("ConcreteMediator", "START")
