import ActionTree.StockActions as actions

import ViDE.Project.Artifacts.CPlusPlus
import ViDE.Project.Artifacts.Fortran
import ViDE.Project.Artifacts.Binary
import ViDE.Project.Artifacts.Python
from ViDE.Buildkit import Buildkit
from ViDE.Core import SubprocessFoo as Subprocess


def SystemAction(args, otherArgs, **kwds):
    return actions.CallSubprocess(*(args + otherArgs))


class Gcc( Buildkit ):
    def canBeDefault( self ):
        return True

    # Flavour specific
    def getDebugCompilationOptions( self ):
        return [ "-g" ]

    def getTestCompilationOptions( self ):
        return self.getDebugCompilationOptions() + [ "--coverage" ]

    def getReleaseCompilationOptions( self ):
        return [ "-O3" ]

    def getDebugLinkOptions( self ):
        return [ "-g" ]

    def getTestLinkOptions( self ):
        return self.getDebugLinkOptions() + [ "--coverage" ]

    def getReleaseLinkOptions( self ):
        return []
    # End (Flavour specific)

    # Target-platform specific
    def getCygwinDynamicLibraryLinkOptions( self ):
        return [ "-shared" ]

    def getWindowsDynamicLibraryLinkOptions( self ):
        return [ "-shared" ]

    def getLinuxDynamicLibraryLinkOptions( self ):
        return [ "-shared" ]
    # End (Target-platform specific)

    class CPlusPlus:
        class Object( ViDE.Project.Artifacts.CPlusPlus.Object ):
            def __init__( self, context, source, additionalDefines, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.fileName( "obj", source.getFileName() + ".o" )
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
                    self.context.flavour.getCompilationOptions()
                    # + self.context.targetPlatform.getCompilationOptions()
                    + [ "-std=c++11" ]
                    + [ "-fPIC" ]
                    + [ "-o", self.__fileName ]
                    + [ "-D" + name for name in self.__additionalDefines ]
                    + [ "-I" + self.context.fileName( "inc" ) ]
                    + [ "-I" + d for d in self.getIncludeDirectories() ],
                    context = self.context
                )

            def getFileName( self ):
                return self.__fileName

    class Fortran:
        class Object( ViDE.Project.Artifacts.Fortran.Object ):
            def __init__( self, context, source, explicit ):
                self.__fileName = context.fileName( "obj", source.getFileName() + ".o" )
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
                    [ "-o" + self.__fileName ],
                    context = self.context
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
                return [ Gcc.Fortran.Object.FakeLibrary( "gfortranbegin" ), Gcc.Fortran.Object.FakeLibrary( "gfortran" ) ] + ViDE.Project.Artifacts.Fortran.Object.getLibrariesToLink( self )

    class Binary:
        class Executable( ViDE.Project.Artifacts.Binary.Executable ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.targetPlatform.computeExecutableName( name )
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
                    self.context.flavour.getLinkOptions()
                    + [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.fileName( "lib" ) ]
                    + [ "-L" + self.context.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ],
                    context = self.context
                )

            def debug( self, arguments ):
                Subprocess.execute( [ "gdb", self.__fileName ] + arguments, context = self.context )

            def valgrind( self ):
                Subprocess.execute( [ "valgrind", "--leak-check=full", self.__fileName ], context = self.context )

        class DynamicLibraryBinary( ViDE.Project.Artifacts.Binary.DynamicLibraryBinary ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.targetPlatform.computeDynamicLibraryName( name )
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
                    [ "g++" ]
                    + self.context.targetPlatform.getDynamicLibraryLinkOptions()
                    +[ "-o", self.__fileName ],
                    self.context.flavour.getLinkOptions()
                    + [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.fileName( "lib" ) ]
                    + [ "-L" + self.context.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ],
                    context = self.context
                )

        class StaticLibraryBinary( ViDE.Project.Artifacts.Binary.StaticLibraryBinary ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                self.__fileName = context.fileName( "lib", "lib" + name + ".a" )
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
                    [ o.getFileName() for o in self.__objects ],
                    context = self.context
                )

    class Python:
        class CModule( ViDE.Project.Artifacts.Python.CModule ):
            def __init__( self, context, name, objects, localLibraries, externalLibraries, explicit ):
                names = name.split( "." )
                names[ -1 ] += "." + context.targetPlatform.getCppPythonModuleExtension()
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
                    [ "g++", "-shared", "-o", self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + self.context.fileName( "lib" ) ]
                    + [ "-L" + self.context.fileName( "bin" ) ]
                    + [ "-L" + lib.getLibPath() for lib in self.getLibrariesToLink() if lib.getLibPath() is not None ]
                    + [ "-l" + lib.getLibName() for lib in self.getLibrariesToLink() ],
                    context = self.context
                )
