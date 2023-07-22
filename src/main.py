from listener import WindowListener
from timer import ProgramTimer, Saver

listener_proc = WindowListener()
listener_proc.start()

timer_proc = ProgramTimer()
timer_proc.start()

saver_proc = Saver()
saver_proc.start()



listener_proc.join()