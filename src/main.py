from listener import WindowListener
from timer import ProgramTimer, Saver

saver_proc = Saver()
timer_proc = ProgramTimer()
listener_proc = WindowListener()

saver_proc.start()
timer_proc.start()
listener_proc.start()

listener_proc.join()
timer_proc.join()
saver_proc.join()