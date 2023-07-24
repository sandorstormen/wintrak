from collections import defaultdict
import os
from pathlib import Path
from typing import Optional, Union
import Xlib
from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

from threading import Thread
from utils import PortMap, Sender, Receiver


class ProgramTimer(Thread):

    def __init__(self, authkey: Optional[bytes] = None) -> None:
        super().__init__()
        self.receiver = Receiver(port=PortMap.TIMER, authkey=authkey)
        self.sender = Sender(port=PortMap.FRONTEND, authkey=authkey)

    def run(self) -> None:
        prev_msg = None

        while True:
            msg = self.receiver.recieve()
            if prev_msg is not None:
                window_title, process_name, current_time = msg
                prev_window_title, prev_process_name, prev_time = prev_msg
                if not (window_title == prev_window_title):
                    new_record = {"WindowTitle": prev_window_title, "ProcessName": prev_process_name, "StartTime": prev_time, "EndTime": current_time}
                    self.sender.send(new_record)
            prev_msg = msg

class Saver(Thread):

    def __init__(self, authkey: Optional[bytes] = None, data_path: Path = Path("data.csv")) -> None:
        super().__init__()
        self.receiver = Receiver(port=PortMap.FRONTEND, authkey=authkey)

        if os.path.exists(data_path):
            self.file_handle = open(data_path, "a")
        else:
            self.file_handle = open(data_path, "w")
            self.file_handle.write("WindowTitle,ProcessName,StartTime,EndTime\n")
            self.file_handle.flush()

    def run(self) -> None:
        while True:
            msg = self.receiver.recieve()
            record = ','.join([str(x).replace(',', '') for x in msg.values()])
            self.file_handle.write(record + "\n")
            self.file_handle.flush()