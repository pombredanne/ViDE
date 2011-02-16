import os.path

from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Core.Actions import CopyFileAction

class CopiedHeader( AtomicArtifact ):
    def __init__( self, buildkit, header ):
        self.__header = header
        self.__copiedHeader = buildkit.fileName( "inc", header.getFileName() )
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
    def __init__( self, buildkit, name, headers ):
        copiedHeaders = [ CopiedHeader( buildkit, header ) for header in headers ]
        CompoundArtifact.__init__( self, name = name + "_hdr", componants = copiedHeaders )
