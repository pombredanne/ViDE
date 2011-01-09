from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Core.Actions import SystemAction

# Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html

class DynamicLibraryBinary( AtomicArtifact ):
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

class DynamicLibrary( CompoundArtifact ):
    def __init__( self, name, objects ):
        self.__binary = DynamicLibraryBinary( name, objects )
        CompoundArtifact.__init__( self, name = name, componants = [ self.__binary ], automatic = False )
        
    def getBinary( self ):
        return self.__binary
