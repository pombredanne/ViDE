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
        return self.getCached( "fetchArtifact", self.__computeFetchArtifact )

    def __computeFetchArtifact( self ):
        componants = [ tool.getFetchArtifact() for tool in self.getTools() ]
        return CompoundArtifact( "tools", componants, False )

    def getInstallArtifact( self ):
        return self.getCached( "installArtifact", self.__computeInstallArtifact )

    def __computeInstallArtifact( self ):
        componants = [ self.__getToolInstallArtifact( tool ) for tool in self.getTools() ]
        componants += [ tool.getFetchArtifact() for tool in self.getTools() ]
        return CompoundArtifact( "tools", componants, False )

    def __getToolInstallArtifact( self, tool ):
        return self.getCached( "installArtifacts", self.__computeToolInstallArtifact, tool )

    def __computeToolInstallArtifact( self, tool ):
        strongDependencies = [ self.__getToolInstallArtifact( self.__toolsByClass[ dep ] ) for dep in tool.getDependencies() ]
        strongDependencies.append( tool.getFetchArtifact() )
        return tool.getInstallArtifact( strongDependencies )
