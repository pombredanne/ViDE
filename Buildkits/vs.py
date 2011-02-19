import ViDE.Project.CPlusPlus
import ViDE.Project.Binary
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
                self.__objects = objects
                ViDE.Project.Binary.Executable.__init__(
                    self,
                    buildkit,
                    name = name,
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "lib" ) ] # Static libraries
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "bin" ) ] # Dynamic libraries # @todo Put the .dll in bin, but the .lib and .exp in lib
                    + [ lib.getLibName() + ".lib" for lib in self.getLibrariesToLink() ]
                )

        class DynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
            def __init__( self, buildkit, name, objects, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "bin", name + ".dll" )
                self.__objects = objects
                ViDE.Project.Binary.DynamicLibraryBinary.__init__(
                    self,
                    buildkit,
                    name = name + "_bin",
                    # @todo Put the .dll in bin, but the .lib and .exp in lib
                    files = [ self.__fileName, self.__buildkit.fileName( "bin", name + ".lib" ), self.__buildkit.fileName( "bin", name + ".exp" ) ],
                    objects = objects,
                    localLibraries = localLibraries
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/DLL", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "lib" ) ] # Static libraries
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "bin" ) ] # Dynamic libraries # @todo Put the .dll in bin, but the .lib and .exp in lib
                    + [ lib.getLibName() + ".lib" for lib in self.getLibrariesToLink() ]
                )

        class StaticLibraryBinary( ViDE.Project.Binary.StaticLibraryBinary ):
            def __init__( self, buildkit, name, objects, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "lib", name + ".lib" )
                self.__objects = objects
                ViDE.Project.Binary.StaticLibraryBinary.__init__(
                    self,
                    buildkit,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "lib", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                )
