#multi threading

#to start jarvis
def startjarvis() :
    print("process 1 is running")
    from main import start
    start()
#to start the hotword detection
def listenhotword():
    print("process 2 is running")
    from engine.features import hotword
    hotword()