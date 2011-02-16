import os
import shutil
import subprocess
import time

from ViDE.Core.Action import Action, LongAction, NullAction
from ViDE import Log

class RemoveFileAction( Action ):
    def __init__( self, file ):
        Action.__init__( self )
        self.__file = file
        
    def shadowClone( self ):
        return RemoveFileAction( self.__file )

    def computePreview( self ):
        return "rm -f " + self.__file
        
    def doExecute( self ):
        try:
            os.unlink( self.__file )
        except OSError:
            pass

class CreateDirectoryAction( Action ):
    __all = dict() # @todo Remove this static variable. Unicity must be managed at client level

    @staticmethod
    def getOrCreate( directory ):
        if directory not in CreateDirectoryAction.__all:
            CreateDirectoryAction.__all[ directory ] = CreateDirectoryAction( directory )
        return CreateDirectoryAction.__all[ directory ]

    def __init__( self, directory ):
        Action.__init__( self )
        self.__directory = directory
        
    def shadowClone( self ):
        return CreateDirectoryAction( self.__directory )

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
    
    def shadowClone( self ):
        return CopyFileAction( self.__originFile, self.__destinationFile )

    def computePreview( self ):
        return "cp " + self.__originFile + " " + self.__destinationFile
        
    def doExecute( self ):
        shutil.copyfile( self.__originFile, self.__destinationFile )
        # @todo Fix work-around
        time.sleep( 1 ) # Race condition ? Microsoft cl doesn't see the file when called just after the copy...

class SystemAction( LongAction ):
    def __init__( self, base, options = [] ):
        LongAction.__init__( self )
        self.__base = base
        self.__options = options
        
    def shadowClone( self ):
        return SystemAction( self.__base, self.__options )
    
    def computePreview( self ):
        return " ".join( self.__base )
        
    def doExecute( self ):
        Log.info( self.computePreview() )
        Log.debug( " ".join( self.__base + self.__options ) )
        subprocess.check_call( self.__base + self.__options )
        Log.verbose( "End of", self.computePreview() )
