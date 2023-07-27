from __future__ import annotations

from wintrak.listener import WindowListener
from wintrak.timer import ProgramTimer


def run():
    timer_proc = ProgramTimer()
    listener_proc = WindowListener()

    timer_proc.start()
    listener_proc.start()

    listener_proc.join()
    timer_proc.join()


if __name__ == "__main__":
    run()
