import os
import stat
import shutil
import time
import sys
import urlparse
import urllib
import tarfile
import zipfile

from ViDE.Core.Action import Action, NullAction
from ViDE.Core import Subprocess
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
        #return "wget " + self.__originUrl
        urlComponents = urlparse.urlparse( self.__originUrl )
        return "wget " + urlComponents.scheme + "://" + urlComponents.netloc + "/[...]/" + os.path.basename( urlComponents.path )

    def doExecute( self ):
        Log.info( self.computePreview() )
        urllib.urlretrieve( self.__originUrl, self.__destinationFile, DownloadFileAction.Hook() )
        print

class SystemAction( Action ):
    def __init__( self, base, options = [], wd = None, buildkit = None, toolset = None ):
        Action.__init__( self )
        self.__base = base
        self.__options = options
        self.__wd = wd
        self.__buildkit = buildkit
        self.__toolset = toolset

    def computePreview( self ):
        return " ".join( self.__base )

    def doExecute( self ):
        Subprocess.execute( self.__base, self.__options, self.__wd, self.__buildkit, self.__toolset )

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

def ActionAndTouch( action, marker ):
    return ActionSequence( [ action, TouchAction( [ marker ] ) ] )

class UnarchiveAction( Action ):
    def __init__( self, archive, destination ):
        Action.__init__( self )
        self.__archive = archive
        self.__destination = destination
        
    def computePreview( self ):
        return "unzip " + self.__archive

    def doExecute( self ):
        buildDirectory = os.path.dirname( self.__destination )
        if tarfile.is_tarfile( self.__archive ):
            archive = tarfile.open( self.__archive )
            unarchiveDirectory = os.path.join( buildDirectory, os.path.commonprefix( [ m.name for m in archive.getmembers() if m.name.find( "PaxHeader" ) == -1 ] ) )
            archive.extractall( buildDirectory )
        elif zipfile.is_zipfile( self.__archive ):
            archive = zipfile.ZipFile( self.__archive )
            unarchiveDirectory = os.path.join( buildDirectory, os.path.commonprefix( archive.namelist() ) )
            archive.extractall( buildDirectory )
        else:
            raise Exception( "Don't know how to extract " + self.__archive )
        os.rename( unarchiveDirectory, self.__destination )
        os.chmod( self.__destination, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH )
        os.utime( self.__destination, None )
