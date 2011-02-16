import os.path

from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from Library import CopiedHeaders

class StaticLibraryBinary( AtomicArtifact ):
    pass

class StaticLibrary( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, headers, binary ):
        return "lib" + name

    def __init__( self, buildkit, name, headers, binary ):
        self.__libName = name
        self.__binary = binary
        self.__copiedHeaders = CopiedHeaders( buildkit, name, headers )
        CompoundArtifact.__init__( self, name = "lib" + name, componants = [ self.__binary, self.__copiedHeaders ] )
        
    def getLibName( self ):
        return self.__libName
        
    def getBinary( self ):
        return self.__binary

    def getCopiedHeaders( self ):
        return self.__copiedHeaders
