import ctypes
import logging

class Awake:
    def __init__(self):
        self.status = False
        self.keep_screen_on = False
        logging.info("Awake process started.")
        self._change_awake_status(self.status)

    def _change_awake_status(self, status):
        # ES_CONTINUOUS & ES_SYSTEM_REQUIRED : 0x80000001
        # ES_CONTINUOUS & ES_DISPLAY_REQUIRED : 0x80000002
        # ES_CONTINUOUS : 0x80000000 (return tu normal)
        if status:
            es_flags = 0x80000002 if self.keep_screen_on else 0x80000001
        else:
            es_flags = 0x80000000

        ctypes.windll.kernel32.SetThreadExecutionState(es_flags)

        logging.info("SetThreadExecutionState: 0x%X", es_flags)

        self.status = status

    def change_status(self):
        self._change_awake_status(not self.status)

    def __del__(self):
        logging.info("Awake process ended.")
        self._change_awake_status(False)