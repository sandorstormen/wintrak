from collections import defaultdict
import os
from pathlib import Path
from typing import Union
import Xlib
from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

from mpi4py import MPI
from threading import Thread
import pandas as pd

from utils import COMMAdress


class ProgramTimer(Thread):

    def __init__(self) -> None:
        super().__init__()
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

    def run(self) -> None:
        prev_msg = None

        while True:
            msg = self.comm.recv(source=0, tag=COMMAdress.TIMER)
            if prev_msg is not None:
                window_title, process_name, current_time = msg
                prev_window_title, prev_process_name, prev_time = prev_msg
                if not (window_title == prev_window_title) and not (process_name == prev_process_name):
                    new_record = {"WindowTitle": prev_window_title, "ProcessName": prev_process_name, "StartTime": prev_time, "EndTime": current_time}
                    self.comm.isend(new_record, dest=0, tag=COMMAdress.FRONTEND)
            prev_msg = msg

class Saver(Thread):

    def __init__(self, data_path: Path = "data.csv") -> None:
        super().__init__()
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

        if os.path.exists(data_path):
            self.file_handle = open(data_path, "a")
        else:
            self.file_handle = open(data_path, "w")
            self.file_handle.write("WindowTitle,ProcessName,StartTime,EndTime\n")
            self.file_handle.flush()

    def run(self) -> None:
        while True:
            msg = self.comm.recv(source=0, tag=COMMAdress.FRONTEND)
            record = ','.join([str(x).replace(',', '') for x in msg.values()])
            self.file_handle.write(record + "\n")
            self.file_handle.flush()