import logging

from cm.TrayIcon import TrayIcon

def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.DEBUG)
    trayIcon = TrayIcon()
    trayIcon.run()

if __name__ == '__main__':
    main()