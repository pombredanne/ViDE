import os.path

from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Core.Actions import CopyFileAction

class DynamicLibraryBinary( AtomicArtifact ):
    pass

class CopiedHeader( AtomicArtifact ):
    def __init__( self, header ):
        self.__header = header
        self.__copiedHeader = os.path.join( os.path.join( "build", "gcc", "inc" ), header.getFileName() ) # @todo Fix this bad work-around (the literal "gcc")
        AtomicArtifact.__init__(
            self,
            name = self.__copiedHeader,
            files = [ self.__copiedHeader ],
            strongDependencies = [ header ],
            orderOnlyDependencies = [],
            automaticDependencies = []
        )
        
    def doGetProductionAction( self ):
        return CopyFileAction( self.__header.getFileName(), self.__copiedHeader )
        
class CopiedHeaders( CompoundArtifact ):
    def __init__( self, name, headers ):
        copiedHeaders = []
        for header in headers:
            copiedHeaders.append( CopiedHeader( header ) )
        CompoundArtifact.__init__( self, name = name + "_hdr", componants = copiedHeaders )
        
class DynamicLibrary( CompoundArtifact ):
    def __init__( self, name, headers, binary ):
        self.__libName = name
        self.__binary = binary
        self.__copiedHeaders = CopiedHeaders( name, headers )
        CompoundArtifact.__init__( self, name = "lib" + name, componants = [ self.__binary, self.__copiedHeaders ] )
        
    def getLibName( self ):
        return self.__libName
        
    def getBinary( self ):
        return self.__binary

    def getCopiedHeaders( self ):
        return self.__copiedHeaders
