import urlparse
import os.path
import multiprocessing

import ViDE
from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction, ActionSequence, UnarchiveAction

class UnarchiveConfigureMakeMakeinstall( AtomicArtifact ):
    def __init__( self, toolset, toolName, archive, strongDependencies, configureOptions = [] ):
        self.__toolset = toolset
        self.__toolName = toolName
        self.__archive = archive
        self.__configureOptions = configureOptions
        AtomicArtifact.__init__(
            self,
            name = toolName,
            files = [ toolName ],
            strongDependencies = strongDependencies,
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )
        
    def doGetProductionAction( self ):
        path = os.path.join( self.__toolset.getTempDirectory(), self.__toolName )
        return ActionSequence( [
            UnarchiveAction( os.path.join( ViDE.toolsCacheDirectory, self.__archive ), path ),
            SystemAction( [ "./configure" ], [ "--prefix=" + os.path.realpath( self.__toolset.getInstallDirectory() ) ] + self.__configureOptions, wd = path ),
            SystemAction( [ "make" ], [ "-j" + str( multiprocessing.cpu_count() + 1 ) ], wd = path ),
            SystemAction( [ "make", "install" ], wd = path ),
        ] )
