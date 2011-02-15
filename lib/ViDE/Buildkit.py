import os.path

class Buildkit:
    def __init__( self, name ):
        self.__name = name
        
    def fileName( self, *nameParts ):
        return os.path.join( "build", self.__name, *nameParts )
