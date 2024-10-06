import logging

import pystray
from PIL import Image
import importlib.resources
import tempfile
import threading

from cm.Awake import Awake
from cm.ClipManager import Clipboard


class TrayIcon:
    def __init__(self):
        self._icon = None
        self._clipboard = None
        self._awake = Awake()

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem('Debug mode', lambda: self._set_loglevel(logging.DEBUG)),
            pystray.MenuItem('Info mode', lambda: self._set_loglevel(logging.INFO)),
            pystray.MenuItem('Start CM', lambda: self._run_clipboard_manager(self._icon)),
            pystray.MenuItem('Stop CM', lambda: self._clipboard.stop()),
            pystray.MenuItem('Start/Stop awake', lambda: self._change_awake_status()),
            pystray.MenuItem('View logfile', lambda: self._view_logfile()),
            pystray.MenuItem('Quit', lambda: self.stop()))

        file = str(importlib.resources.files().joinpath('data/cm.png'))
        image = Image.open(file)

        self._icon = pystray.Icon("CM", image, "Clipboard Manager", menu=menu)
        self._clipboard = Clipboard(trigger_at_start=False)
        self._icon.run(self._run_clipboard_manager)

    def _change_awake_status(self):
        self._awake.change_status()
        if self._awake.status:
            self._icon.icon = Image.open(str(importlib.resources.files().joinpath('data/caffeine.png')))
        else:
            self._icon.icon = Image.open(str(importlib.resources.files().joinpath('data/cm.png')))
        pass

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
        logFile = tempfile.gettempdir() + '\\cm.log'
        tailprog = str(importlib.resources.files().joinpath('data/SnakeTail.exe'))
        cmd = '"{}" "{}"'.format(tailprog, logFile)
        import subprocess
        subprocess.Popen([tailprog, logFile], shell=False)

    def stop(self):
        self._icon.visible = False
        self._clipboard.stop()
        self._icon.stop()
