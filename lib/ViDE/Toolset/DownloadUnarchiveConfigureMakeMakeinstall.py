import urlparse
import os.path
import multiprocessing

import ViDE
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Core.Actions import SystemAction, DownloadFileAction, UnarchiveAction, ActionAndTouch

def DownloadUnarchiveConfigureMakeMakeinstall( toolset, downloadOnly, toolName, archiveUrl, strongDependencies, configureOptions = [] ):
    downloaded = DownloadedArchive( archiveUrl )
    if downloadOnly:
        return downloaded
    else:
        unarchived = UnarchivedArchive( toolset, toolName, downloaded )
        configured = ConfiguredPackage( toolset, toolName, configureOptions, strongDependencies, unarchived )
        made = MadePackage( toolset, toolName, configured )
        installed = InstalledPackage( toolset, toolName, made )
        return CompoundArtifact( toolName, [ downloaded, unarchived, configured, made, installed ], False )

class DownloadedArchive( AtomicArtifact ):
    def __init__( self, url ):
        self.__url = url
        self.__file = os.path.join( ViDE.toolsCacheDirectory, os.path.basename( urlparse.urlparse( url ).path ) )
        AtomicArtifact.__init__(
            self,
            name = self.__file,
            files = [ self.__file ],
            strongDependencies = [],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return DownloadFileAction( self.__url, self.__file )

    def getFile( self ):
        return self.__file

class UnarchivedArchive( AtomicArtifact ):
    def __init__( self, toolset, toolName, downloadedArchive ):
        self.__toolset = toolset
        self.__toolName = toolName
        self.__downloadedArchive = downloadedArchive
        self.__marker = os.path.join( self.__toolset.getMarkerDirectory(), toolName + "_unarchived"  )
        self.__destination = os.path.join( self.__toolset.getTempDirectory(), self.__toolName )
        AtomicArtifact.__init__(
            self,
            name = self.__marker,
            files = [ self.__marker ],
            strongDependencies = [ downloadedArchive ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return ActionAndTouch(
            UnarchiveAction( self.__downloadedArchive.getFile(), self.__destination ),
            self.__marker
        )
        
    def getDestination( self ):
        return self.__destination

class ConfiguredPackage( AtomicArtifact ):
    def __init__( self, toolset, toolName, configureOptions, strongDependencies, unarchivedArchive ):
        self.__toolset = toolset
        self.__configureOptions = configureOptions
        self.__unarchivedArchive = unarchivedArchive
        self.__marker = os.path.join( toolset.getMarkerDirectory(), toolName + "_configured"  )
        AtomicArtifact.__init__(
            self,
            name = self.__marker,
            files = [ self.__marker ],
            strongDependencies = strongDependencies + [ unarchivedArchive ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return ActionAndTouch(
            SystemAction(
                [ "./configure" ],
                [ "--prefix=" + os.path.realpath( self.__toolset.getInstallDirectory() ) ] + self.__configureOptions,
                wd = self.getDestination(),
                toolset = self.__toolset
            ),
            self.__marker
        )
        
    def getDestination( self ):
        return self.__unarchivedArchive.getDestination()

class MadePackage( AtomicArtifact ):
    def __init__( self, toolset, toolName, configuredPackage ):
        self.__toolset = toolset
        self.__configuredPackage = configuredPackage
        self.__marker = os.path.join( toolset.getMarkerDirectory(), toolName + "_made"  )
        AtomicArtifact.__init__(
            self,
            name = self.__marker,
            files = [ self.__marker ],
            strongDependencies = [ configuredPackage ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return ActionAndTouch(
            SystemAction(
                [ "make" ],
                [ "-j" + str( multiprocessing.cpu_count() + 1 ) ],
                wd = self.getDestination(),
                toolset = self.__toolset
            ),
            self.__marker
        )

    def getDestination( self ):
        return self.__configuredPackage.getDestination()

class InstalledPackage( AtomicArtifact ):
    def __init__( self, toolset, toolName, madePackage ):
        self.__toolset = toolset
        self.__madePackage = madePackage
        self.__marker = os.path.join( toolset.getMarkerDirectory(), toolName + "_installed"  )
        AtomicArtifact.__init__(
            self,
            name = self.__marker,
            files = [ self.__marker ],
            strongDependencies = [ madePackage ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return ActionAndTouch(
            SystemAction(
                [ "make", "install" ],
                wd = self.getDestination(),
                toolset = self.__toolset
            ),
            self.__marker
        )

    def getDestination( self ):
        return self.__madePackage.getDestination()
