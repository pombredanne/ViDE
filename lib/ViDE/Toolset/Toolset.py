import imp
import sys
import os.path

import ViDE

class Toolset:
    @classmethod
    def load( cls, toolsetName ):
        oldSysPath = sys.path
        sys.path.append( ViDE.toolsDirectory )
        toolset = getattr( imp.load_source( toolsetName, os.path.join( ViDE.toolsetsDirectory, toolsetName + ".py" ) ), toolsetName )
        sys.path = oldSysPath
        return toolset

    def __init__( self, *tools ):
        self.__tools = tools
