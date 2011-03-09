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
        componants = []
        for tool in self.getTools():
            componants.append( tool.getInstallArtifact() )
        return CompoundArtifact( "tools", componants, False )
