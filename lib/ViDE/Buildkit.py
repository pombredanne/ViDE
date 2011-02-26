import imp
import os.path

import ViDE

class Buildkit:
    @classmethod
    def load( cls, buildkitName, *args ):
        return getattr( imp.load_source( buildkitName, os.path.join( ViDE.buildkitsDirectory, buildkitName + ".py" ) ), buildkitName )( buildkitName, *args )

    def __init__( self, name ):
        self.__name = name
        
    def fileName( self, *nameParts ):
        return os.path.join( "build", self.__name, *( self.getPreliminaryNameParts() + list( nameParts ) ) )
