import sys
import os.path
import imp
import glob

import ViDE

class Loadable:
    @classmethod
    def load( cls, name, *args, **kwargs ):
        if name == "" or name is None:
            return cls.__loadDefault( *args, **kwargs )
        else:
            return cls.__loadByName( name, *args, **kwargs )

    @classmethod
    def __loadByName( cls, name, *args, **kwargs ):
        assert( name is not None )
        oldSysPath = sys.path
        loadDirectory = cls.__computeLoadDirectory()
        sys.path.append( loadDirectory )
        instance = getattr( imp.load_source( name, os.path.join( loadDirectory, name + ".py" ) ), name )( *args, **kwargs )
        sys.path = oldSysPath
        return instance

    @classmethod
    def __loadDefault( cls, *args, **kwargs ):
        default = None
        for instance in cls.__loadAll( *args, **kwargs ):
            if instance.canBeDefault():
                if default is None:
                    default = instance
                else:
                    raise Exception( "Could not choose default between " + cls.__name__ + "s " + default.name + " and " + instance.name )
        if default is None:
            raise Exception( "Could not find default " + cls.__name__ )
        # print "Choosing default " + cls.__name__ + ": " + default.name
        return default

    @classmethod
    def __loadAll( cls, *args, **kwargs ):
        loadDirectory = cls.__computeLoadDirectory()
        all = []
        for file in glob.glob( os.path.join( loadDirectory, "*.py" ) ):
            name = os.path.basename( file )[ : -3 ]
            all.append( cls.__loadByName( name, *args, **kwargs ) )
        return all

    @classmethod
    def __computeLoadDirectory( cls ):
        return os.path.join( ViDE.rootDirectory(), "Loadables", cls.__name__ + "s" )

    def __init__( self ):
        self.name = self.__class__.__name__
