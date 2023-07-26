from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime
from multiprocessing.pool import ThreadPool
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import Xlib
from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

from threading import Lock, Thread
from utils import PortMap, Sender, Receiver


class ProgramTimer(Thread):
    def __init__(self, authkey: Optional[bytes] = None) -> None:
        super().__init__()
        self.receiver = Receiver(port=PortMap.TIMER, authkey=authkey)
        self.saver = Saver()

    def run(self) -> None:
        prev_msg = None

        while True:
            msg = self.receiver.recieve()
            if prev_msg is not None:
                window_title, process_name, current_time = msg
                prev_window_title, prev_process_name, prev_time = prev_msg
                if not (window_title == prev_window_title):
                    new_record = {
                        "WindowTitle": prev_window_title,
                        "ProcessName": prev_process_name,
                        "StartTime": prev_time,
                        "EndTime": current_time,
                    }
                    self.saver.save(new_record)
            prev_msg = msg


class Saver:
    def __init__(
        self, data_path: Path = Path("~") / ".local" / "share" / "WinTrak" / "data.csv"
    ) -> None:
        super().__init__()

        data_path = data_path.expanduser()
        data_path.parent.mkdir(parents=True, exist_ok=True)
        if not data_path.exists():
            self.file_handle = open(data_path, "w")
            self.file_handle.write("WindowTitle,ProcessName,StartTime,EndTime\n")
            self.file_handle.flush()
            self.file_handle.close()

        self.lock = Lock()

    def save(self, record: Dict[str, str | datetime]) -> None:
        thread = SaveThread(self.lock, record)
        thread.start()
        return


class SaveThread(Thread):
    def __init__(
        self,
        lock: Lock,
        record: Dict[str, str | datetime],
        data_path: Path = Path("~") / ".local" / "share" / "WinTrak" / "data.csv",
    ) -> None:
        super().__init__()

        self.lock = lock
        self.record = record
        self.data_path = data_path.expanduser()

    def run(self) -> None:
        csv_string = ",".join([str(x).replace(",", "") for x in self.record.values()])
        with self.lock:
            with open(self.data_path, "a") as file_handle:
                file_handle.write(csv_string + "\n")
                file_handle.flush()
