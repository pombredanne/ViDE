# Standard library
import os.path

# Project
from ViDE.Core.Loadable import Loadable
from ViDE.ContextReferer import ContextReferer

class Toolset( Loadable, ContextReferer ):
    def __init__( self, context ):
        Loadable.__init__( self )
        ContextReferer.__init__( self, context )
        self.__toolsByClass = dict()
        for tool in self.computeTools():
            if tool.__class__ in self.__toolsByClass:
                raise Exception( "Same tool two times in toolset" )
            self.__toolsByClass[ tool.__class__ ] = tool

    def getTool( self, toolClass ):
        return self.__toolsByClass[ toolClass ]
