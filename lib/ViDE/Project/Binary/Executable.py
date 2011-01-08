from ViDE.Core.Artifact import AtomicArtifact, SystemAction

class Executable( AtomicArtifact ):
    def __init__( self, name ):
        AtomicArtifact.__init__( self, name, [ "build/bin/" + name ], [], [], False )
        self.__name = name

    def doGetProductionAction( self ):
        return SystemAction( "g++ -o build/bin/" + self.__name )
