import logging
import tempfile
from logging.handlers import TimedRotatingFileHandler

from cm.TrayIcon import TrayIcon

def main():
    logFile = tempfile.gettempdir() + '\\cm.log'
    handler = TimedRotatingFileHandler(logFile,
                                       when="d",
                                       interval=1,
                                       backupCount=5)

    logging.basicConfig(handlers=[handler], format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.DEBUG)
    trayIcon = TrayIcon()
    trayIcon.run()

if __name__ == '__main__':
    main()