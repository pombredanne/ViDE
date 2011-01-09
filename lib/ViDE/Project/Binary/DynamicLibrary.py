from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import SystemAction

# Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html

class DynamicLibrary( AtomicArtifact ):
    def __init__( self, name, objects ):
        self.__libName = name
        self.__fileName = "build/lib/" + name + ".dll"
        self.__objects = objects
        AtomicArtifact.__init__(
            self,
            name = "lib" + name,
            files = [ self.__fileName ],
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automatic = False
        )
        
    def getLibName( self ):
        return self.__libName

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-shared", "-o" + self.__fileName ] + [ o.getFileName() for o in self.__objects ], "g++ -o " + self.__fileName )
