from ViDE.Core.Actions import CopyFileAction
from ViDE.Core.Artifact import InputArtifact, AtomicArtifact

class MonofileInputArtifact( InputArtifact ):
    @staticmethod
    def computeName( buildkit, fileName, explicit ):
        return fileName

    def __init__( self, buildkit, fileName, explicit ):
        InputArtifact.__init__( self, name = fileName, files = [ fileName ], explicit = explicit )
        self.__fileName = fileName
        
    def getFileName( self ):
        return self.__fileName

class CopiedArtifact( AtomicArtifact ):
    @staticmethod
    def computeName( buildkit, source, destination, explicit ):
        return destination

    def __init__( self, buildkit, source, destination, explicit ):
        self.__source = source
        self.__destination = destination
        AtomicArtifact.__init__(
            self,
            name = destination,
            files = [ destination ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )
    
    def doGetProductionAction( self ):
        return CopyFileAction( self.__source.getFileName(), self.__destination )

    def getDestination( self ):
        return self.__destination

    def getSource( self ):
        return self.__source
