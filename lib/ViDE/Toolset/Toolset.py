import imp
import sys
import os.path

import ViDE
from ViDE.Core.CallOnceAndCache import CallOnceAndCache
from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Core.Loadable import Loadable

class Toolset( Loadable, CallOnceAndCache ):
    def __init__( self ):
        Loadable.__init__( self )
        CallOnceAndCache.__init__( self )
        self.__toolsByClass = dict()
        for tool in self.getTools():
            if tool.__class__ in self.__toolsByClass:
                raise Exception( "Same tool two times in toolset" )
            self.__toolsByClass[ tool.__class__ ] = tool

    def getTools( self ):
        return self.getCached( "tools", self.computeTools )

    def getFetchArtifact( self ):
        return self.getCached( "fetchArtifact", self.__computeInstallArtifact, downloadOnly = True )

    def getInstallArtifact( self ):
        return self.getCached( "installArtifact", self.__computeInstallArtifact, downloadOnly = False )

    def __computeInstallArtifact( self, downloadOnly ):
        componants = [ self.__getToolInstallArtifact( tool, downloadOnly ) for tool in self.getTools() ]
        return CompoundArtifact( "tools", componants, False )

    def __getToolInstallArtifact( self, tool, downloadOnly ):
        return self.getCached( "installArtifacts", self.__computeToolInstallArtifact, tool, downloadOnly )

    def __computeToolInstallArtifact( self, tool, downloadOnly ):
        if downloadOnly:
            strongDependencies = []
        else:
            strongDependencies = [ self.__getToolInstallArtifact( self.__toolsByClass[ dep ], downloadOnly ) for dep in tool.getDependencies() ]
        return tool.getInstallArtifact( self, downloadOnly, strongDependencies )

    def getTempDirectory( self ):
        return os.path.join( ViDE.toolsetsTmpDirectory(), self.__class__.__name__ )

    def getInstallDirectory( self ):
        return os.path.join( ViDE.toolsetsInstallDirectory(), self.__class__.__name__ )

    def getMarkerDirectory( self ):
        return os.path.join( ViDE.toolsetsMarkerDirectory(), self.__class__.__name__ )
