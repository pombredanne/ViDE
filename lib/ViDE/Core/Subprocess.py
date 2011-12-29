import subprocess
import os

from ViDE import Log

def execute( base, options = [], wd = None, context = None ):
    SubProcess( base, options, wd, context ).execute()

class SubProcess:
    def __init__( self, base, options, wd, context ):
        self.__base = base
        self.__options = options
        self.__wd = wd
        self.__context = context
        self.__preview = " ".join( base )

    def execute( self ):
        Log.info( self.__preview )
        Log.debug( " ".join( self.__base + self.__options ) )
        try:
            self.__updateEnviron()
            self.__changeWorkingDirectory()
            self.__setIoStreams()
            self.__execute()
        finally:
            self.__restoreEnviron()
            self.__restoreWorkingDirectory()

    def __updateEnviron( self ):
        self.__oldEnviron = dict( os.environ )
        if self.__context is not None:
            # @todo Do not override PYTHONPATH if it already exists
            os.environ[ "PYTHONPATH" ] = self.__context.fileName( "pyd" )
            os.environ[ "LD_LIBRARY_PATH" ] = self.__context.fileName( "lib" )
            os.environ[ "PATH" ] = os.path.realpath( os.path.join( self.__context.toolset.getInstallDirectory(), "bin" ) ) + ":" + os.environ[ "PATH" ]

    def __changeWorkingDirectory( self ):
        if self.__wd is not None:
            self.__oldWorkingDirectory = os.getcwd()
            os.chdir( self.__wd )

    def __setIoStreams( self ):
        self.__stdout = None
        if Log.level < 1:
            self.__stdout = subprocess.PIPE
        self.__stderr = None
        if Log.level < 0:
            self.__stderr = subprocess.PIPE

    def __execute( self ):
        p = subprocess.Popen( self.__base + self.__options, stdout = self.__stdout, stderr = self.__stderr )
        p.communicate()
        if p.returncode == 0:
            Log.verbose( "End of", self.__preview )
        else:
            Log.verbose( "Error during", self.__preview )
            raise Exception( "Error during " + self.__preview )

    def __restoreWorkingDirectory( self ):
        if self.__wd is not None:
            os.chdir( self.__oldWorkingDirectory )

    def __restoreEnviron( self ):
        os.environ = self.__oldEnviron
