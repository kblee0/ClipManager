import importlib.resources
import logging
import subprocess
import sys
import tempfile
import winreg

import pystray
from PIL import Image

from cm.Awake import Awake
from cm.ClipManager import Clipboard


class TrayIcon:
    def __init__(self):
        self._icon = None
        self._clipboard = Clipboard(trigger_at_start=False)
        self._clipboard.listen()
        self._awake = Awake()
        self._icon_images = []
        self._icon_images.append(Image.open(str(importlib.resources.files().joinpath('data/cm.png'))))
        self._icon_images.append(Image.open(str(importlib.resources.files().joinpath('data/caffeine.png'))))

    @property
    def _create_menu(self) -> pystray.Menu:
        menu = pystray.Menu(
            pystray.MenuItem('Autorun at login', lambda: self._menu_register_autorun(), checked=lambda item: self._autorun_setting(0), radio=True),
            pystray.MenuItem('Stop CM listener' if self._clipboard.is_listening() else 'Start CM', lambda: self._menu_cm_listening()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Stop awake' if self._awake.status else 'Start awake', lambda: self._menu_awake_status(), default=True),
            pystray.MenuItem('Keep screen on', lambda: self._menu_keep_screen_on(), checked=lambda item: self._awake.keep_screen_on, radio=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Text Only', lambda: self._clipboard.toogle_text_only(), checked=lambda item: self._clipboard._text_only, radio=True),
            pystray.MenuItem('View logfile', lambda: self._view_logfile()),
            pystray.MenuItem('Set log level to ' + ('DEBUG' if logging.getLogger().level == logging.INFO else 'INFO'), lambda: self._menu_loglevel()),
            pystray.MenuItem('Clear Clipboard', lambda: self._clipboard.clear_clipboard()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Quit', lambda: self.stop()))
        return menu

    def run(self):
        self._icon = pystray.Icon("CM", self._icon_images[0], "Clipboard Manager", menu=self._create_menu)
        self._icon.run()

    def _menu_cm_listening(self):
        self._clipboard.stop() if self._clipboard.is_listening() else self._clipboard.listen()
        self._icon.menu = self._create_menu

    def _menu_awake_status(self):
        self._awake.toggle_status()
        self._icon.icon = self._icon_images[1] if self._awake.status else self._icon_images[0]
        self._icon.menu = self._create_menu

    def _menu_keep_screen_on(self):
        self._awake.keep_screen_on = not self._awake.keep_screen_on
        if self._awake.status: self._awake.set_awake_status(True)

    def _menu_loglevel(self):
        level = logging.INFO if logging.getLogger().level == logging.DEBUG else logging.DEBUG
        logging.getLogger().setLevel(level)
        self._icon.menu = self._create_menu

    def _autorun_setting(self, mode):
        name = "CM.1.0"
        result = True
        try:
            keypath = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
            if mode == 0:
                result = winreg.QueryValueEx(keypath, name) == (sys.executable, winreg.REG_SZ)
            elif mode == 1:
                winreg.SetValueEx(keypath, name, 0, winreg.REG_SZ, sys.executable)
            else:
                winreg.DeleteValue(keypath, name)
            winreg.CloseKey(keypath)
            return result
        except FileNotFoundError:
            return False

    def _menu_register_autorun(self):
        if self._autorun_setting(0):
            self._autorun_setting(2)
        else:
            self._autorun_setting(1)

    @staticmethod
    def _view_logfile():
        log_file = tempfile.gettempdir() + '\\cm.log'
        tail_pgm = str(importlib.resources.files().joinpath('data/SnakeTail.exe'))

        subprocess.Popen([tail_pgm, log_file], shell=False)

    def stop(self):
        self._icon.visible = False
        self._clipboard.stop()
        self._icon.stop()
