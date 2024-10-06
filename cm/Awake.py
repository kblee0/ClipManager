import ctypes
import logging

class Awake:
    def __init__(self):
        self.status = False
        self._change_awake_status(self.status)

    def _change_awake_status(self, status):
        if status:
            # ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # keep awake ES_CONTINUOUS & ES_DISPLAY_REQUIRED
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)  # keep awake ES_CONTINUOUS & ES_SYSTEM_REQUIRED
            logging.info("SetThreadExecutionState: 0x80000002")
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # return to normal
            logging.info("SetThreadExecutionState: 0x80000000")
        self.status = status

    def change_status(self):
        self._change_awake_status(not self.status)

    def __del__(self):
        self._change_awake_status(False)

