import urlparse
import os.path

import ViDE
from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction, ActionSequence, UnarchiveAction

class UnarchiveConfigureMakeMakeinstall( AtomicArtifact ):
    def __init__( self, archive, file, strongDependencies, configureOptions = [] ):
        self.__archive = archive
        self.__configureOptions = configureOptions
        AtomicArtifact.__init__(
            self,
            name = file,
            files = [ file ],
            strongDependencies = strongDependencies,
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )
        
    def doGetProductionAction( self ):
        return ActionSequence( [
            UnarchiveAction( self.__archive ),
            SystemAction( [ "./configure" ], self.__configureOptions )
        ] )
