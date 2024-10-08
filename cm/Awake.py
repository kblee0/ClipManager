import ctypes
import logging

class Awake:
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002  # return tu normal
    def __init__(self):
        self.status = False
        self.keep_screen_on = False
        logging.info("Awake process started.")
        self.set_awake_status(self.status)

    def set_awake_status(self, status):
        if status:
            es_flags = Awake.ES_CONTINUOUS | Awake.ES_DISPLAY_REQUIRED if self.keep_screen_on else Awake.ES_CONTINUOUS | Awake.ES_SYSTEM_REQUIRED
        else:
            es_flags = Awake.ES_CONTINUOUS

        ctypes.windll.kernel32.SetThreadExecutionState(es_flags)

        logging.info("SetThreadExecutionState: 0x%X", es_flags)

        self.status = status

    def toggle_status(self):
        self.set_awake_status(not self.status)

    def __del__(self):
        logging.info("Awake process ended.")
        self.set_awake_status(False)