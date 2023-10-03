import threading
import os

def thread_function1():
    os.system("python3 consumers.py")

def thread_function2():
    os.system("python3 manage.py runserver 0.0.0.0:8000")


x = threading.Thread(target=thread_function1)
y = threading.Thread(target=thread_function2)
T = [x, y]

for t in T:
    t.start()
    
for t in T:
    t.join()