import os
import shutil
import subprocess

from ViDE.Core.Action import Action, LongAction
from ViDE import Log

class NullAction( Action ):
    def __init__( self, preview = "" ):
        Action.__init__( self )
        self.__preview = preview

    def doExecute( self ):
        pass

    def computePreview( self ):
        return self.__preview

class RemoveFileAction( Action ):
    def __init__( self, file ):
        Action.__init__( self )
        assert( isinstance( self, Action ) )
        self.__file = file

    def computePreview( self ):
        return "rm -f " + self.__file
        
    def doExecute( self ):
        try:
            os.unlink( self.__file )
        except OSError:
            pass

class CreateDirectoryAction( Action ):
    __all = dict()

    @staticmethod
    def getOrCreate( directory ):
        if directory not in CreateDirectoryAction.__all:
            CreateDirectoryAction.__all[ directory ] = CreateDirectoryAction( directory )
        return CreateDirectoryAction.__all[ directory ]

    def __init__( self, directory ):
        Action.__init__( self )
        self.__directory = directory

    def computePreview( self ):
        return "mkdir -p " + self.__directory
        
    def doExecute( self ):
        try:
            os.makedirs( self.__directory )
        except OSError:
            pass

class CopyFileAction( Action ):
    def __init__( self, originFile, destinationFile ):
        Action.__init__( self )
        self.__originFile = originFile
        self.__destinationFile = destinationFile

    def computePreview( self ):
        return "cp " + self.__originFile + " " + self.__destinationFile
        
    def doExecute( self ):
        shutil.copyfile( self.__originFile, self.__destinationFile )

class SystemAction( LongAction ):
    def __init__( self, command, preview ):
        LongAction.__init__( self )
        self.__command = command
        self.__preview = preview
    
    def computePreview( self ):
        return self.__preview
        
    def doExecute( self ):
        Log.info( self.__preview )
        Log.debug( " ".join( self.__command ) )
        subprocess.check_call( self.__command )
        Log.verbose( "End of", self.__preview )
