import logging
import tempfile
from logging.handlers import TimedRotatingFileHandler

from tendo import singleton

from cm.trayicon import TrayIcon


def main():
    me = singleton.SingleInstance()
    log_file = tempfile.gettempdir() + '\\cm.log'
    file_handler = TimedRotatingFileHandler(log_file,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    logging.basicConfig(handlers=[file_handler,console_handler], format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    logging.info("----------------------------------------------")
    logging.info("ClipboardManager starting")
    tray_icon = TrayIcon()
    tray_icon.run()

if __name__ == "__main__":
    main()