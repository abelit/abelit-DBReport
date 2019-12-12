import threading
import time

def _deamon():
    while True:
        print('hello')

        time.sleep(2)


t = threading.Thread(target=_deamon)
t.setDaemon(False)

t.start()

print("end the process")
