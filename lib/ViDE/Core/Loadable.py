import sys
import os.path
import imp

import ViDE

class Loadable:
    @classmethod
    def load( cls, name, *args, **kwargs ):
        oldSysPath = sys.path
        sys.path.append( ViDE.toolsDirectory )
        instance = getattr( imp.load_source( name, os.path.join( ViDE.rootDirectory, cls.__name__ + "s", name + ".py" ) ), name )( *args, **kwargs )
        sys.path = oldSysPath
        return instance

    def __init__( self ):
        self.name = self.__class__.__name__
        