import urlparse
import os.path

import ViDE
from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Action import NullAction

class UnarchiveConfigureMakeMakeinstall( AtomicArtifact ):
    def __init__( self, configureOptions = [] ):
        file = "configure"
        AtomicArtifact.__init__(
            self,
            name = file,
            files = [ file ],
            strongDependencies = [],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )
        
    def doGetProductionAction( self ):
        return NullAction( "blah" )
