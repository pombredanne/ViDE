import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class gcc( ViDE.Buildkit.Buildkit ):
    class CPlusPlus:
        class Object( ViDE.Project.CPlusPlus.Object ):
            @staticmethod
            def computeName( buildkit, source, additionalDefines, localLibraries ):
                return buildkit.fileName( "obj", source.getFileName() + ".o" )
            
            def __init__( self, buildkit, source, additionalDefines, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "obj", source.getFileName() + ".o" )
                self.__additionalDefines = additionalDefines
                ViDE.Project.CPlusPlus.Object.__init__( self, buildkit, [ self.__fileName ], source, localLibraries )

            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "g++", "-c", sourceName ],
                    [ "-I" + self.__buildkit.fileName( "inc" ), "-o" + self.__fileName ]
                    + [ "-D" + name for name in self.__additionalDefines ]
                )

            def getFileName( self ):
                return self.__fileName

    class Binary:
        class Executable( ViDE.Project.Binary.Executable ):
            @staticmethod
            def computeName( buildkit, name, objects, localLibraries ):
                return name
            
            def __init__( self, buildkit, name, objects, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "bin", name )
                ViDE.Project.Binary.Executable.__init__( self, buildkit, name, [ self.__fileName ], objects, localLibraries )
                self.__localLibraries = localLibraries
                self.__objects = objects

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "g++", "-o" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.__buildkit.fileName( "lib" ) ]
                    + [ "-l" + lib.getLibName() for lib in self.__localLibraries ]
                )

        class DynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
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

        class StaticLibraryBinary( ViDE.Project.Binary.StaticLibraryBinary ):
            def __init__( self, buildkit, name, objects ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "lib", "lib" + name + ".a" )
                self.__objects = objects
                ViDE.Project.Binary.StaticLibraryBinary.__init__(
                    self,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    strongDependencies = objects,
                    orderOnlyDependencies = [],
                    automaticDependencies = []
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "ar", "-q", self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                )
