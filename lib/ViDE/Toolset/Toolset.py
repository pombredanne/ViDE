import os.path

import ViDE
from ViDE.Core.CallOnceAndCache import CallOnceAndCache
from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Core.Loadable import Loadable
from ViDE.ContextReferer import ContextReferer

class Toolset( Loadable, CallOnceAndCache, ContextReferer ):
    def __init__( self, context ):
        Loadable.__init__( self )
        CallOnceAndCache.__init__( self )
        ContextReferer.__init__( self, context )
        self.__toolsByClass = dict()
        for tool in self.getTools():
            if tool.__class__ in self.__toolsByClass:
                raise Exception( "Same tool two times in toolset" )
            self.__toolsByClass[ tool.__class__ ] = tool

    def getTools( self ):
        return self.getCached( "tools", self.computeTools )

    def getTool( self, toolClass ):
        return self.__toolsByClass[ toolClass ]
