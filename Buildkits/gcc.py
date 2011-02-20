import ViDE.Project.CPlusPlus
import ViDE.Project.Binary
import ViDE.Project.Python
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class gcc( ViDE.Buildkit.Buildkit ):
    class CPlusPlus:
        class Object( ViDE.Project.CPlusPlus.Object ):
            @staticmethod
            def computeName( buildkit, source, additionalDefines, localLibraries, explicit ):
                return buildkit.fileName( "obj", source.getFileName() + ".o" )

            def __init__( self, buildkit, source, additionalDefines, localLibraries, explicit ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "obj", source.getFileName() + ".o" )
                self.__additionalDefines = additionalDefines
                ViDE.Project.CPlusPlus.Object.__init__(
                    self,
                    buildkit = buildkit,
                    files = [ self.__fileName ],
                    source = source,
                    localLibraries = localLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "g++", "-c", sourceName ],
                    [ "-I" + self.__buildkit.fileName( "inc" ), "-o" + self.__fileName ]
                    + [ "-D" + name for name in self.__additionalDefines ]
                    + [ "-I/usr/include/python2.6" ]
                )

            def getFileName( self ):
                return self.__fileName

    class Binary:
        class Executable( ViDE.Project.Binary.Executable ):
            @staticmethod
            def computeName( buildkit, name, objects, localLibraries, explicit ):
                return name

            def __init__( self, buildkit, name, objects, localLibraries, explicit ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "bin", name + ".exe" )
                self.__objects = objects
                ViDE.Project.Binary.Executable.__init__(
                    self,
                    buildkit,
                    name = name,
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "g++", "-o" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.__buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.__buildkit.fileName( "bin" ) ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                )

        class DynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
            def __init__( self, buildkit, name, objects, localLibraries, explicit ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "bin", name + ".dll" )
                self.__objects = objects
                ViDE.Project.Binary.DynamicLibraryBinary.__init__(
                    self,
                    buildkit,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                # Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html
                return SystemAction(
                    [ "g++", "-shared", "-o" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.__buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.__buildkit.fileName( "bin" ) ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                )

        class StaticLibraryBinary( ViDE.Project.Binary.StaticLibraryBinary ):
            def __init__( self, buildkit, name, objects, localLibraries, explicit ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "lib", "lib" + name + ".a" )
                self.__objects = objects
                ViDE.Project.Binary.StaticLibraryBinary.__init__(
                    self,
                    buildkit,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "ar", "-q", self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                )

    class Python:
        class CModule( ViDE.Project.Python.CModule ):
            @staticmethod
            def computeName( buildkit, name, objects, localLibraries, explicit ):
                return name

            def __init__( self, buildkit, name, objects, localLibraries, explicit ):
                self.__buildkit = buildkit
                names = name.split( "." )
                names[ -1 ] += ".dll"
                self.__fileName = self.__buildkit.fileName( "pyd", *names )
                self.__objects = objects
                ViDE.Project.Python.CModule.__init__(
                    self,
                    buildkit,
                    name = self.__fileName,
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "g++", "-shared", "-o" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.__buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.__buildkit.fileName( "bin" ) ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                    + [ "-lpython2.6" ]
                )
