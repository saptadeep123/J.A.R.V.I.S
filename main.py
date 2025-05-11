import os
import eel

from engine.features import *
from engine.command import*
from root import listenhotword, startjarvis

def start():
    eel.init("frontend")

    playassistentsound()

    os.system('start chrome --app="http://localhost:8000/index.html"')
    eel.start('index.html',mode=None,host='localhost',block=True)


#starting both processes
import multiprocessing
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=startjarvis)
    p2 = multiprocessing.Process(target=listenhotword)
    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("system stop")



