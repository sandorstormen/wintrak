import logging
import Xlib
from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

from mpi4py import MPI
from threading import Thread
from datetime import datetime
import psutil

from utils import COMMAdress

class WindowListener(Thread):

    def __init__(self) -> None:
        super().__init__()
        self.disp = Display()
        Xroot = self.disp.screen().root
        self._NET_ACTIVE_WINDOW = self.disp.intern_atom("_NET_ACTIVE_WINDOW")
        self._NET_WM_NAME = self.disp.intern_atom("_NET_WM_NAME")
        self._NET_WM_PID = self.disp.intern_atom("_NET_WM_PID")
        Xroot.change_attributes(
            event_mask=Xlib.X.PropertyChangeMask | Xlib.X.SubstructureNotifyMask
        )
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

    def _get_window_title(self, window: Window):
        return window.get_full_text_property(self._NET_WM_NAME)

    def send_active_window(self):
        current_time = datetime.now()
        active: Window = self.disp.get_input_focus().focus
        window_title = active.get_full_text_property(self._NET_WM_NAME)
        pid = active.get_full_property(self._NET_WM_PID, X.AnyPropertyType)
        process = psutil.Process(pid.value[0])
        process_name = process.name()
        self.comm.isend((window_title, process_name, current_time), dest=0, tag=COMMAdress.TIMER)


    def run(self) -> None:
        self.send_active_window()
        while True:
            event = self.disp.next_event()
            if event.type == Xlib.X.PropertyNotify and event.atom == self._NET_ACTIVE_WINDOW:
                try:
                    self.send_active_window()
                except Exception as e:
                    logging.error(e)
                    pass