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

    def computePreview( self ):
        return "rm -f " + self.__file
        
    def doExecute( self ):
        try:
            os.unlink( self.__file )
        except OSError:
            pass

class CreateDirectoryAction( Action ):
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
        # @todo Fix work-around
        time.sleep( 1 ) # Race condition ? Microsoft cl doesn't see the file when called just after the copy...

class SystemAction( LongAction ):
    def __init__( self, base, options = [] ):
        LongAction.__init__( self )
        self.__base = base
        self.__options = options
    
    def computePreview( self ):
        return " ".join( self.__base )
        
    def doExecute( self ):
        Log.info( self.computePreview() )
        Log.debug( " ".join( self.__base + self.__options ) )
        p = subprocess.Popen( self.__base + self.__options, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
        stdoutdata, stderrdata = p.communicate()
        stdoutdata = stdoutdata.strip()
        stderrdata = stderrdata.strip()
        if stdoutdata != "":
            Log.info( stdoutdata )
        if stderrdata != "":
            Log.error( stderrdata )
        if p.returncode == 0:
            Log.verbose( "End of", self.computePreview() )
        else:
            Log.verbose( "Error during", self.computePreview() )
            raise Exception( "Error during " + self.computePreview() )

class TouchAction( Action ):
    def __init__( self, files ):
        Action.__init__( self )
        self.__files = files

    def computePreview( self ):
        return "touch " + " ".join( self.__files )

    def doExecute( self ):
        now = time.time()
        time.sleep( 0.1 ) # Ensure files will be more recent than any other touched files
        for file in self.__files:
            # Inspired from http://code.activestate.com/recipes/576915-touch/
            try:
                os.utime( file, ( now, now ) )
            except os.error:
                open( file, "w" ).close()
                os.utime( file, ( now, now ) )
