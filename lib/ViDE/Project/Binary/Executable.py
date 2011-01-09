import os.path

from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction

class Executable( AtomicArtifact ):
    def __init__( self, name, objects, localLibraries ):
        self.__fileName = os.path.join( "build", "bin", name )
        AtomicArtifact.__init__(
            self,
            name = name,
            files = [ self.__fileName ],
            strongDependencies = objects,
            orderOnlyDependencies = [ lib.getBinary() for lib in localLibraries ],
            automaticDependencies = [],
            automatic = False
        )
        self.__name = name
        self.__objects = objects
        self.__localLibraries = localLibraries

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-o" + self.__fileName ] + [ o.getFileName() for o in self.__objects ] + [ "-L" + os.path.join( "build", "lib" ) ] + [ "-l" + lib.getLibName() for lib in self.__localLibraries ], "g++ -o " + self.__fileName )
