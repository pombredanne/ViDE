import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class vs( ViDE.Buildkit.Buildkit ):
    class CPlusPlus:
        class Object( ViDE.Project.CPlusPlus.Object ):
            @staticmethod
            def computeName( buildkit, source, additionalDefines, localLibraries ):
                return buildkit.fileName( "obj", source.getFileName() + ".obj" )

            def __init__( self, buildkit, source, additionalDefines, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "obj", source.getFileName() + ".obj" )
                self.__additionalDefines = additionalDefines
                ViDE.Project.CPlusPlus.Object.__init__( self, buildkit, [ self.__fileName ], source, localLibraries )
        
            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "cl", "/c", sourceName ],
                    [ "/EHsc", "/I" + self.__buildkit.fileName( "inc" ), "/Fo" + self.__fileName ]
                    + [ "/D" + name for name in self.__additionalDefines ]
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
                self.__fileName = self.__buildkit.fileName( "bin", name + ".exe" )
                ViDE.Project.Binary.Executable.__init__( self, buildkit, name, [ self.__fileName ], objects, localLibraries )
                self.__localLibraries = localLibraries
                self.__objects = objects
            
            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "bin" ) ]
                    + [ lib.getLibName() + ".lib" for lib in self.__localLibraries ]
                )

        class DynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
            def __init__( self, buildkit, name, objects ):
                self.__buildkit = buildkit
                self.__objects = objects
                self.__libName = self.__buildkit.fileName( "bin", name + ".dll" )
                ViDE.Project.Binary.DynamicLibraryBinary.__init__(
                    self,
                    name = name + "_bin",
                    files = [ self.__buildkit.fileName( "bin", name + ".dll" ), self.__buildkit.fileName( "bin", name + ".lib" ), self.__buildkit.fileName( "bin", name + ".exp" ) ],
                    strongDependencies = objects,
                    orderOnlyDependencies = [],
                    automaticDependencies = []
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/DLL", "/OUT:" + self.__libName ],
                    [ o.getFileName() for o in self.__objects ]
                )
