import threading

lock = threading.Lock()

level = 1

def error( *args ):
    if level >= 0:
        log( *args )

def info( *args ):
    if level >= 1:
        log( *args )

def verbose( *args ):
    if level >= 2:
        log( *args )

def debug( *args ):
    if level >= 3:
        log( *args )

def log( *args ):
    with lock:
        for arg in args:
            print arg,
        print
