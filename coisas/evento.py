import threading
import time

exit = threading.Event()
while not exit.wait(timeout=0.01):
    print("a")
    x = input("oooi")
    if x == "a":
        exit.set()
print("saiu")
