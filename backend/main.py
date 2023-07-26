from wintrak.listener import WindowListener
from wintrak.timer import ProgramTimer

timer_proc = ProgramTimer()
listener_proc = WindowListener()

timer_proc.start()
listener_proc.start()

listener_proc.join()
timer_proc.join()