import subprocess
import os
from time import sleep
import termios
import sys

# create stdin pipe
pipe_read, pipe_write = os.pipe2(0)

# create a vim subprocess
child_pid = os.fork()
if child_pid == 0:
    os.dup2(pipe_read,sys.stdin.fileno())
    os.execlp("vim","vim")

# setup parent terminal
old_term_attrs = termios.tcgetattr(sys.stdin.fileno())
new_term_attrs = termios.tcgetattr(sys.stdin.fileno())
new_term_attrs[3] = new_term_attrs[3] & ~termios.ECHO
termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,new_term_attrs)
try:
    while True:
        sleep(0.5)
        os.write(pipe_write,b":q\n")
        if os.waitpid(child_pid,os.WNOHANG) != (0,0):
            break
except KeyboardInterrupt:
    pass
finally:
    termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,old_term_attrs)
