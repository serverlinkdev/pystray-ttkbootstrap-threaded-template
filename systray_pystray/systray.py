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
import logging
import threading

import pystray
from PIL import Image
from pystray import MenuItem as item

from mediator.base_component import BaseComponent


class Systray(BaseComponent):
    """
    A class using the Mediator design pattern.

    User's of this class should only:
    - Instantiate
    - Set mediator
    - Call in to this class using 'notify' method.
    """

    _app_icon = None
    _app_name = None
    _image = None
    mediator = None
    _menu = None
    _systray = None

    def __init__(self, app_icon, app_name):
        """
        Args:
        app_icon (str): the icon you want to see in your desktop OS
        app_name (str): the name of the app you want to see in OS notification's
        """
        super().__init__()
        # by default, PIL is chatty.
        logging.getLogger('PIL').setLevel(logging.WARNING)
        self._app_icon = app_icon
        self._app_name = app_name
        self._create_tray()

    def notify(self, sender, event):
        if sender == "ConcreteMediator":
            if event == "START":
                # start the systray thread and put the icon in user's OS tray
                self._start_systray()

    def _create_tray(self):
        """
        Build the Systray
        """
        # smile icon from breeze icon theme ubuntu 23.10
        self._image = Image.open(self._app_icon)
        self._menu = (
            item('Quit', self._quit_main_window),
            item('Show', self._show_main_window))
        self._systray = pystray.Icon("name",
                                     self._image,
                                     self._app_name,
                                     self._menu)

    def _quit_main_window(self):
        """
        Tell's ConcreteMediator that we need to quit the MainWindow.
        Stop's the Systray from running.
        """
        self.mediator.notify(self, "QUIT")
        self._systray.visible = False
        self._systray.stop()
        logging.info("Goodbye from Systray!")

    def _run_systray(self):
        """
        Runs the Systray continuously.
        """
        while True:
            self._systray.run()

    def _show_main_window(self):
        """
        Tell's ConcreteMediator to show the MainWindow
        """
        self.mediator.notify(self, "SHOW")

    def _start_systray(self):
        """
        Create a thread to run the Systray in
        """
        thread = threading.Thread(
            daemon=True,
            target=lambda: self._run_systray()
        )
        thread.start()
