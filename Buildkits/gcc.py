import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class CPlusPlusObject( ViDE.Project.CPlusPlus.Object ):
    def __init__( self, buildkit, source, localLibraries ):
        self.__buildkit = buildkit
        self.__fileName = self.__buildkit.fileName( "obj", source.getFileName() + ".o" )
        ViDE.Project.CPlusPlus.Object.__init__( self, [ self.__fileName ], source, localLibraries )

    def doGetProductionAction( self ):
        sourceName = self.getSource().getFileName()
        return SystemAction(
            [ "g++", "-c", sourceName ],
            [ "-I" + self.__buildkit.fileName( "inc" ), "-o" + self.__fileName ]
        )

    def getFileName( self ):
        return self.__fileName

class BinaryExecutable( ViDE.Project.Binary.Executable ):
    def __init__( self, buildkit, name, objects, localLibraries ):
        self.__buildkit = buildkit
        self.__fileName = self.__buildkit.fileName( "bin", name )
        ViDE.Project.Binary.Executable.__init__( self, name, [ self.__fileName ], objects, localLibraries )
        self.__localLibraries = localLibraries
        self.__objects = objects

    def doGetProductionAction( self ):
        return SystemAction(
            [ "g++", "-o" + self.__fileName ],
            [ o.getFileName() for o in self.__objects ]
            + [ "-L" + self.__buildkit.fileName( "lib" ) ]
            + [ "-l" + lib.getLibName() for lib in self.__localLibraries ]
        )

class BinaryDynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
    def __init__( self, buildkit, name, objects ):
        self.__buildkit = buildkit
        self.__fileName = self.__buildkit.fileName( "lib", name + ".dll" )
        self.__objects = objects
        ViDE.Project.Binary.DynamicLibraryBinary.__init__(
            self,
            name = name + "_bin",
            files = [ self.__fileName ],
            strongDependencies = objects,
            orderOnlyDependencies = [],
            automaticDependencies = []
        )

    def doGetProductionAction( self ):
        # Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html
        return SystemAction(
            [ "g++", "-shared", "-o" + self.__fileName ],
            [ o.getFileName() for o in self.__objects ]
        )

class CPlusPlusFactory:
    def __init__( self, buildkit ):
        self.__buildkit = buildkit

    def Object( self, *args ):
        return CPlusPlusObject( self.__buildkit, *args )

class BinaryFactory:
    def __init__( self, buildkit ):
        self.__buildkit = buildkit

    def Executable( self, *args ):
        return BinaryExecutable( self.__buildkit, *args )

    def DynamicLibraryBinary( self, *args ):
        return BinaryDynamicLibraryBinary( self.__buildkit, *args )

class gcc( ViDE.Buildkit.Buildkit ):
    def __init__( self, name ):
        ViDE.Buildkit.Buildkit.__init__( self, name )
        self.CPlusPlus = CPlusPlusFactory( self )
        self.Binary = BinaryFactory( self )
