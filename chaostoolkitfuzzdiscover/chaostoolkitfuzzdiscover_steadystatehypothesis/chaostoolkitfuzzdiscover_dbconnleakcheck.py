import threading
import time

def loop1_10():
    for i in range(1, 7):
        time.sleep(1)
        print(i)

def loopa_z():
    for i in range(20, 25):
        time.sleep(1)
        print '*'

a = threading.Thread(target=loop1_10)

b = threading.Thread(target=loopa_z)
a.start()
b.start()
print a.is_alive()
print b.is_alive()
exit(1)
a.join()
b.join()
print a.is_alive()
print b.is_alive()


print threading.currentThread()
