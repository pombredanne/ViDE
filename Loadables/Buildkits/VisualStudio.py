import ViDE.Project.Artifacts.CPlusPlus
import ViDE.Project.Artifacts.Binary
import ViDE.Project.Artifacts.Python
from ViDE.Core.Actions import SystemAction
from ViDE.Buildkit import Buildkit

class VisualStudio( Buildkit ):
    def canBeDefault( self ):
        return False

    class CPlusPlus:
        class Object( ViDE.Project.Artifacts.CPlusPlus.Object ):
            def __init__( self, context, source, additionalDefines, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.fileName( "obj", source.getFileName() + ".obj" )
                self.__additionalDefines = additionalDefines
                ViDE.Project.Artifacts.CPlusPlus.Object.__init__(
                    self,
                    context = context,
                    files = [ self.__fileName ],
                    source = source,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "cl", "/c", sourceName ]
                    + [ "/Fo" + self.__fileName ]
                    + [ "/EHsc" ]
                    + [ "/D" + name for name in self.__additionalDefines ]
                    + [ "/I" + self.context.fileName( "inc" ) ]
                    + [ "/I" + d for d in self.getIncludeDirectories() ],
                    [],
                    context = self.context
                )

            def getFileName( self ):
                return self.__fileName

    class Binary:
        class Executable( ViDE.Project.Artifacts.Binary.Executable ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.fileName( "bin", name + ".exe" )
                self.__objects = objects
                ViDE.Project.Artifacts.Binary.Executable.__init__(
                    self,
                    context = context,
                    name = name,
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.context.fileName( "lib" ) ] # Static libraries
                    + [ "/LIBPATH:" + self.context.fileName( "bin" ) ] # Dynamic libraries # @todo Put the .dll in bin, but the .lib and .exp in lib
                    + [ lib.getLibName() + ".lib" for lib in self.getLibrariesToLink() ],
                    context = self.context
                )

            def debug( self, arguments ):
                print "Debuging with Visual Studio is not supported yet"

        class DynamicLibraryBinary( ViDE.Project.Artifacts.Binary.DynamicLibraryBinary ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.fileName( "bin", name + ".dll" )
                self.__objects = objects
                ViDE.Project.Artifacts.Binary.DynamicLibraryBinary.__init__(
                    self,
                    context,
                    name = name + "_bin",
                    # @todo Put the .dll in bin, but the .lib and .exp in lib
                    files = [ self.__fileName, context.fileName( "bin", name + ".lib" ), context.fileName( "bin", name + ".exp" ) ],
                    objects = objects,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/DLL", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.context.fileName( "lib" ) ] # Static libraries
                    + [ "/LIBPATH:" + self.context.fileName( "bin" ) ] # Dynamic libraries # @todo Put the .dll in bin, but the .lib and .exp in lib
                    + [ lib.getLibName() + ".lib" for lib in self.getLibrariesToLink() ],
                    context = self.context
                )

        class StaticLibraryBinary( ViDE.Project.Artifacts.Binary.StaticLibraryBinary ):
            def __init__( self, buildkit, name, objects, localLibraries, explicit ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "lib", name + ".lib" )
                self.__objects = objects
                ViDE.Project.Artifacts.Binary.StaticLibraryBinary.__init__(
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
                    [ "lib", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ],
                    context = self.context
                )

    class Python:
        class CModule( ViDE.Project.Artifacts.Python.CModule ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                names = name.split( "." )
                names[ -1 ] += ".pyd"
                self.__fileName = context.fileName( "pyd", *names )
                self.__objects = objects
                ViDE.Project.Artifacts.Python.CModule.__init__(
                    self,
                    context = context,
                    name = self.__fileName,
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/DLL", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.context.fileName( "lib" ) ] # Static libraries
                    + [ "/LIBPATH:" + self.context.fileName( "bin" ) ] # Dynamic libraries # @todo Put the .dll in bin, but the .lib and .exp in lib
                    + [ "/LIBPATH:" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ lib.getLibName() + ".lib" for lib in self.getLibrariesToLink() ],
                    context = self.context
                )
