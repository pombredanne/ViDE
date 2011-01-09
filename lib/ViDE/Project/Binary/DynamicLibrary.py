import os.path

from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Core.Actions import SystemAction, CopyFileAction

# Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html

class DynamicLibraryBinary( AtomicArtifact ):
    def __init__( self, name, objects ):
        self.__fileName = "build/lib/" + name + ".dll"
        self.__objects = objects
        AtomicArtifact.__init__(
            self,
            name = name + "_bin",
            files = [ self.__fileName ],
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automatic = False
        )

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-shared", "-o" + self.__fileName ] + [ o.getFileName() for o in self.__objects ], "g++ -o " + self.__fileName )

class CopiedHeader( AtomicArtifact ):
    def __init__( self, header ):
        self.__header = header
        self.__copiedHeader = os.path.join( "build/inc", header.getFileName() )
        AtomicArtifact.__init__(
            self,
            name = self.__copiedHeader,
            files = [ self.__copiedHeader ],
            strongDependencies = [ header ],
            orderOnlyDependencies = [],
            automatic = False
        )
        
    def doGetProductionAction( self ):
        return CopyFileAction( self.__header.getFileName(), self.__copiedHeader )
        
class CopiedHeaders( CompoundArtifact ):
    def __init__( self, name, headers ):
        copiedHeaders = []
        for header in headers:
            copiedHeaders.append( CopiedHeader( header ) )
        CompoundArtifact.__init__( self, name = name + "_hdr", componants = copiedHeaders, automatic = False )
        
class DynamicLibrary( CompoundArtifact ):
    def __init__( self, name, headers, objects ):
        self.__libName = name
        self.__binary = DynamicLibraryBinary( name, objects )
        self.__copiedHeaders = CopiedHeaders( name, headers )
        CompoundArtifact.__init__( self, name = "lib" + name, componants = [ self.__binary, self.__copiedHeaders ], automatic = False )
        
    def getLibName( self ):
        return self.__libName
        
    def getBinary( self ):
        return self.__binary

    def getCopiedHeaders( self ):
        return self.__copiedHeaders
