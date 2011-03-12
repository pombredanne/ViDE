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

    def getFetchArtifact( self ):
        componants = []
        for tool in self.getTools():
            componants.append( tool.getFetchArtifact() )
        return CompoundArtifact( "tools", componants, False )

    def getInstallArtifact( self ):
        artifacts = []
        for tool in self.getTools():
            artifacts += self.__getInstallArtifacts( tool )
        return CompoundArtifact( "tools", artifacts, False )

    def __getInstallArtifacts( self, tool ):
        return self.getCached( "fetchArtifact", self.__computeInstallArtifacts, tool )
        
    def __computeInstallArtifacts( self, tool ):
        strongDependencies = []
        for dep in tool.getDependencies():
            strongDependencies += self.__getInstallArtifacts( self.__toolsByClass[ dep ] )
        return [ tool.getInstallArtifact( strongDependencies ) ] + strongDependencies
