import imp
import sys
import os.path

import ViDE
from ViDE.Core.Artifact import CompoundArtifact

class Toolset:
    @classmethod
    def load( cls, toolsetName, *args ):
        oldSysPath = sys.path
        sys.path.append( ViDE.toolsDirectory )
        toolset = getattr( imp.load_source( toolsetName, os.path.join( ViDE.toolsetsDirectory, toolsetName + ".py" ) ), toolsetName )( toolsetName, *args )
        sys.path = oldSysPath
        return toolset

    def __init__( self, tools ):
        self.__tools = tools

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
