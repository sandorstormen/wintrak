import logging
from typing import Optional
import Xlib
from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

from threading import Thread
from datetime import datetime
import psutil

from utils import PortMap, Sender


class WindowListener(Thread):
    def __init__(self, authkey: Optional[bytes] = None) -> None:
        super().__init__()
        self.disp = Display()
        Xroot = self.disp.screen().root
        self._NET_ACTIVE_WINDOW = self.disp.intern_atom("_NET_ACTIVE_WINDOW")
        self._NET_WM_NAME = self.disp.intern_atom("_NET_WM_NAME")
        self._WM_NAME = self.disp.intern_atom("WM_NAME")
        self._NET_WM_PID = self.disp.intern_atom("_NET_WM_PID")
        Xroot.change_attributes(
            event_mask=Xlib.X.PropertyChangeMask | Xlib.X.SubstructureNotifyMask
        )
        self.sender = Sender(port=PortMap.TIMER, authkey=authkey)

    def _get_window_title(self, window: Window):
        return window.get_full_text_property(self._NET_WM_NAME)

    def send_window(self, window_handle: Window):
        current_time = datetime.now()
        event_mask = window_handle.get_attributes()._data["your_event_mask"]
        if event_mask == 0:
            window_handle.change_attributes(event_mask=X.PropertyChangeMask)

        window_title = window_handle.get_full_text_property(self._NET_WM_NAME)
        if window_title is None:
            window_title = window_handle.get_full_text_property(self._WM_NAME)

        pid = window_handle.get_full_property(self._NET_WM_PID, X.AnyPropertyType)
        try:
            process = psutil.Process(pid.value[0])
            process_name = process.name()
        except AttributeError:
            process_name = ""

        self.sender.send((window_title, process_name, current_time))

    def run(self) -> None:
        self.send_window(self.disp.get_input_focus().focus)
        while True:
            event = self.disp.next_event()
            if event.type == X.PropertyNotify and event.atom == self._NET_ACTIVE_WINDOW:
                try:
                    self.send_window(self.disp.get_input_focus().focus)
                except Exception as e:
                    logging.error(e)
                    pass
            elif event.type == X.PropertyNotify and (
                event.atom == self._NET_WM_NAME or event.atom == self._WM_NAME
            ):
                try:
                    self.send_window(event.window)
                except Exception as e:
                    logging.error(e)
                    pass
