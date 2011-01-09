from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction

class Executable( AtomicArtifact ):
    def __init__( self, name, objects, localLibraries ):
        AtomicArtifact.__init__(
            self,
            name = name,
            files = [ "build/bin/" + name ],
            strongDependencies = objects,
            orderOnlyDependencies = [ lib.getBinary() for lib in localLibraries ],
            automatic = False
        )
        self.__name = name
        self.__objects = objects
        self.__localLibraries = localLibraries

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-obuild/bin/" + self.__name ] + [ o.getFileName() for o in self.__objects ] + [ "-Lbuild/lib" ] + [ "-l" + lib.getLibName() for lib in self.__localLibraries ], "g++ -o build/bin/" + self.__name )
