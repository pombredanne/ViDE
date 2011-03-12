import os
import shutil
import subprocess
import time
import sys
import urlparse
import urllib

from ViDE.Core.Action import Action, NullAction
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

class DownloadFileAction( Action ):
    class Hook:
        def __init__( self ):
            self.__partTransfered = 0

        def __call__( self, transferedBlocks, blockSize, totalSize ):
            newPart = self.__part( transferedBlocks, blockSize, totalSize )
            if newPart != self.__partTransfered:
                sys.stdout.write( "-" )
                sys.stdout.flush()
            self.__partTransfered = newPart

        def __part( self, transferedBlocks, blockSize, totalSize ):
            return 80 * transferedBlocks * blockSize / totalSize

    def __init__( self, originUrl, destinationFile ):
        Action.__init__( self )
        self.__originUrl = originUrl
        self.__destinationFile = destinationFile

    def computePreview( self ):
        urlComponents = urlparse.urlparse( self.__originUrl )
        return "wget " + urlComponents.scheme + "://" + urlComponents.netloc + "/[...]/" + os.path.basename( urlComponents.path )

    def doExecute( self ):
        Log.info( self.computePreview() )
        urllib.urlretrieve( self.__originUrl, self.__destinationFile, DownloadFileAction.Hook() )
        print

class SystemAction( Action ):
    def __init__( self, base, options = [] ):
        Action.__init__( self )
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

class ActionSequence( Action ):
    def __init__( self, actions ):
        Action.__init__( self )
        self.__actions = actions

    def computePreview( self ):
        return "; ".join( a.getPreview() for a in self.__actions )

    def doExecute( self ):
        for a in self.__actions:
            a.doExecute()

class UnarchiveAction( Action ):
    def __init__( self, archive ):
        Action.__init__( self )
        self.__archive = archive
        
    def computePreview( self ):
        return "unzip " + self.__archive

    def doExecute( self ):
        pass
