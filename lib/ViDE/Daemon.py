import threading
import subprocess
import os
import glob

daemonLock = threading.Lock() ###@todo Maybe use a lock per project... or even queue and merge OnPush requests. Later :)

class OnPush:
    def __init__( self, directory ):
        self.__directory = directory

    def __call__( self ):
        with daemonLock:
            self.execute()

    def execute( self ):
        for f in glob.glob( os.path.join( self.__directory, "*.git" ) ):
            # subprocess.check_call( [ "git", "--git-dir=" + f, "fetch" ] )
            p = subprocess.Popen( [ "git", "--git-dir=" + f, "branch", "-a" ], stdout = subprocess.PIPE )
            ( out, err ) = p.communicate()
            for branch in out.split( "\n" ):
                branch = branch[2:]
                if len( branch ) != 0:
                    self.executeBranch( f, branch )

    def executeBranch( self, bareGitRepo, branch ):
        workingDirectory = os.path.join( bareGitRepo[:-4], branch )
        if os.path.exists( workingDirectory ):
            subprocess.check_call( [ "git", "--git-dir=" + workingDirectory, "pull" ] )
        else:
            subprocess.check_call( [ "git", "clone", "--branch", branch, bareGitRepo, workingDirectory ] )

class DaemonApp:
    def __init__( self, directory ):
        self.__directory = directory

    def __call__( self, environ, start_response ):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        thread = threading.Thread( target = OnPush( self.__directory ) )
        thread.start()
        start_response( status, headers )
        return [ "OK" ]
