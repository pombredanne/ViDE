from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction

class Executable( AtomicArtifact ):
    def __init__( self, name, objects ):
        AtomicArtifact.__init__(
            self,
            name = name,
            files = [ "build/bin/" + name ],
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automatic = False
        )
        self.__name = name
        self.__objects = objects

    def doGetProductionAction( self ):
        return SystemAction( "g++ -o build/bin/" + self.__name + " " + " ".join( [ o.getFileName() for o in self.__objects ] ) )
