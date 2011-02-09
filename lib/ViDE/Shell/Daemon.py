import wsgiref.simple_server
import time
import threading

import ViDE
from Misc.InteractiveCommandLineProgram import Command

daemonLock = threading.Lock() ###@todo Maybe use a lock per project... or even queue and merge OnPush requests. Later :)

class OnPush:
    def __init__( self, project ):
        self.__project = project
    
    def __call__( self ):
        with daemonLock:
            self.execute()
    
    def execute( self ):
        print "Yatta 1"
        time.sleep( 10 )
        print "Yatta 2"

def DeamonApp( environ, start_response ):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    project = environ[ "PATH_INFO" ].split( "/" )[ -1 ]
    thread = threading.Thread( target = OnPush( project ) )
    thread.start()
    start_response( status, headers )
    return []

class Daemon( Command ):
    def execute( self, args ):
        httpd = wsgiref.simple_server.make_server( '', 8080, DeamonApp )
        httpd.serve_forever()
        #httpd.handle_request()
