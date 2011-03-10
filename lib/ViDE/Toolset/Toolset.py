import imp
import sys
import os.path

import ViDE
from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Core.Loadable import Loadable

class Toolset( Loadable ):
    def __init__( self ):
        Loadable.__init__( self )

    def getFetchArtifact( self ):
        componants = []
        for tool in self.getTools():
            componants.append( tool.getFetchArtifact() )
        return CompoundArtifact( "tools", componants, False )

    def getInstallArtifact( self ):
        artifacts = []
        artifact = None
        for tool in self.getTools():
            # The strongDependencies argument to Tool.getInstallArtifact should be computed with tool dependencies instead
            artifact = tool.getInstallArtifact( [] if artifact is None else [ artifact ] )
            artifacts.append( artifact )
        return CompoundArtifact( "tools", artifacts, False )
