from ViDE.Core import Subprocess
import ViDE.Project.Artifacts.CPlusPlus
import ViDE.Project.Artifacts.Fortran
import ViDE.Project.Artifacts.Binary
import ViDE.Project.Artifacts.Python
from ViDE.Core.Actions import SystemAction
from ViDE.Buildkit import Buildkit

class gcc( Buildkit ):
    class CPlusPlus:
        class Object( ViDE.Project.Artifacts.CPlusPlus.Object ):
            def __init__( self, context, source, additionalDefines, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.buildkit.fileName( "obj", source.getFileName() + ".o" )
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
                    [ "g++", "-c", sourceName ],
                    self.context.buildkit.getCompilationOptions()
                    + [ "-o", self.__fileName ]
                    + [ "-D" + name for name in self.__additionalDefines ]
                    + [ "-I" + self.context.buildkit.fileName( "inc" ) ]
                    + [ "-I" + d for d in self.getIncludeDirectories() ]
                )

            def getFileName( self ):
                return self.__fileName

    class Fortran:
        class Object( ViDE.Project.Artifacts.Fortran.Object ):
            def __init__( self, context, source, explicit ):
                self.__fileName = context.buildkit.fileName( "obj", source.getFileName() + ".o" )
                ViDE.Project.Artifacts.Fortran.Object.__init__(
                    self,
                    context = context,
                    files = [ self.__fileName ],
                    source = source,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "gfortran", "-c", sourceName ],
                    [ "-o" + self.__fileName ]
                )

            def getFileName( self ):
                return self.__fileName
            
            class FakeLibrary:
                def __init__( self, name ):
                    self.__name = name

                def getLibName( self ):
                    return self.__name
                
                def getLibPath( self ):
                    return None

            def getLibrariesToLink( self ):
                return [ gcc.Fortran.Object.FakeLibrary( "gfortranbegin" ), gcc.Fortran.Object.FakeLibrary( "gfortran" ) ] + ViDE.Project.Artifacts.Fortran.Object.getLibrariesToLink( self )

    class Binary:
        class Executable( ViDE.Project.Artifacts.Binary.Executable ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.buildkit.computeExecutableName( context, name )
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
                    [ "g++", "-o", self.__fileName ],
                    self.context.buildkit.getLinkOptions()
                    + [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.context.buildkit.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                )

            def debug( self, arguments ):
                Subprocess.execute( [ "gdb", self.__executableFile ] + arguments, context = self.context )

        class DynamicLibraryBinary( ViDE.Project.Artifacts.Binary.DynamicLibraryBinary ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.buildkit.computeDynamicLibraryName( context, name )
                self.__objects = objects
                ViDE.Project.Artifacts.Binary.DynamicLibraryBinary.__init__(
                    self,
                    context,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                # Build commands taken from http://www.cygwin.com/cygwin-ug-net/dll.html
                return SystemAction(
                    [ "g++", self.context.buildkit.getDynamicLibraryFlag(), "-o", self.__fileName ],
                    self.context.buildkit.getLinkOptions()
                    + [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.context.buildkit.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                )

        class StaticLibraryBinary( ViDE.Project.Artifacts.Binary.StaticLibraryBinary ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.buildkit.fileName( "lib", "lib" + name + ".a" )
                self.__objects = objects
                ViDE.Project.Artifacts.Binary.StaticLibraryBinary.__init__(
                    self,
                    context = context,
                    name = name + "_bin",
                    files = [ self.__fileName ],
                    objects = objects,
                    localLibraries = localLibraries,
                    externalLibraries = externalLibraries,
                    explicit = explicit
                )

            def doGetProductionAction( self ):
                return SystemAction(
                    [ "ar", "-q", self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                )

    class Python:
        class CModule( ViDE.Project.Artifacts.Python.CModule ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                names = name.split( "." )
                names[ -1 ] += ".dll"
                self.__fileName = context.buildkit.fileName( "pyd", *names )
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
                    [ "g++", "-shared", "-o", self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.buildkit.fileName( "lib" ) ]
                    + [ "-L" + self.context.buildkit.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ]
                    + [ "-lpython2.6" ] # @todo Remove
                )
