import logging
import tempfile
from logging.handlers import TimedRotatingFileHandler

from cm.TrayIcon import TrayIcon

def main():
    log_file = tempfile.gettempdir() + '\\cm.log'
    handler = TimedRotatingFileHandler(log_file,
                                       when="d",
                                       interval=1,
                                       backupCount=5)

    logging.basicConfig(handlers=[handler], format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    tray_icon = TrayIcon()
    tray_icon.run()

if __name__ == '__main__':
    main()