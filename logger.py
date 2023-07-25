#
#   Author:
#   Gian Paolo Buenconsejo
#   

import datetime
from tkinter import END, NORMAL, DISABLED

enable_logging = True


class Logger():
    """
    Initialiaze a logger object to log messages.
    """

    def __init__(self, enable=True) -> None:
        self.logs = ""
        self.IsEnabled = enable
        self.field = None

    def set_field(self, field):
        self.field = field

    def log(self, message: str, include_time: bool=True, display_to_console: bool=True) -> str:
        """
        Logs a message into the logger.
        ### Params
        - message: message to log
        - include_time: if to include the time of log
        - display_to_console: if message is to be printed to console
        """
        if not self.IsEnabled:
            return
        
        if include_time:
            log = f"[{datetime.datetime.now().strftime('%X')}] {message}" + "\n"
        else:
            log = f"{message}" + "\n"

        if display_to_console:
            print(log)

        self.logs += log

        if self.field:
            self.field.config(state=NORMAL)
            self.field.insert(END, log)
            self.field.config(state=DISABLED)

        return message
    
    def get_logs(self) -> str:
        return self.logs

logger = Logger(enable_logging)