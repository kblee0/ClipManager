import importlib.resources
import logging
import subprocess
import tempfile
import threading

import pystray
from PIL import Image

from cm.Awake import Awake
from cm.ClipManager import Clipboard


class TrayIcon:
    def __init__(self):
        self._icon = None
        self._clipboard = None
        self._awake = Awake()
        self._icon_images = []
        self._icon_images.append(Image.open(str(importlib.resources.files().joinpath('data/cm.png'))))
        self._icon_images.append(Image.open(str(importlib.resources.files().joinpath('data/caffeine.png'))))

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem('Debug mode', lambda: self._set_loglevel(logging.DEBUG)),
            pystray.MenuItem('Info mode', lambda: self._set_loglevel(logging.INFO)),
            pystray.MenuItem('Start CM', lambda: self._run_clipboard_manager(self._icon)),
            pystray.MenuItem('Stop CM', lambda: self._clipboard.stop()),
            pystray.MenuItem('Start/Stop awake', lambda: self._change_awake_status()),
            pystray.MenuItem('View logfile', lambda: self._view_logfile()),
            pystray.MenuItem('Quit', lambda: self.stop()))

        self._icon = pystray.Icon("CM", self._icon_images[0], "Clipboard Manager", menu=menu)
        self._clipboard = Clipboard(trigger_at_start=False)
        self._icon.run(self._run_clipboard_manager)

    def _change_awake_status(self):
        self._awake.change_status()
        if self._awake.status:
            self._icon.icon = self._icon_images[1]
        else:
            self._icon.icon = self._icon_images[0]

    def _run_clipboard_manager(self, icon):
        self._icon.visible = True

        def clipboard_runner():
            self._clipboard.listen()

        th = threading.Thread(target=clipboard_runner, daemon=True)
        th.start()

    def _stop_clipboard_manager(self):
        self._clipboard.stop()

    @staticmethod
    def _set_loglevel(level):
        logging.getLogger().setLevel(level)

    @staticmethod
    def _view_logfile():
        log_file = tempfile.gettempdir() + '\\cm.log'
        tail_pgm = str(importlib.resources.files().joinpath('data/SnakeTail.exe'))

        subprocess.Popen([tail_pgm, log_file], shell=False)

    def stop(self):
        self._icon.visible = False
        self._clipboard.stop()
        self._icon.stop()
