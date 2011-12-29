import sys

import ViDE.Project.Artifacts.Binary
import ViDE.Project.Artifacts.CPlusPlus
from ViDE.Core.Actions import SystemAction
from ViDE.Buildkit import Buildkit

class Gcc( Buildkit ):
    def canBeDefault( self ):
        return True

    def getDebugCompilationOptions( self ):
        return [ "-g" ]

    def getDebugLinkOptions( self ):
        return [ "-g" ]

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
                    + [ "-o", self.__fileName ]
                    + [ "-D" + name for name in self.__additionalDefines ]
                    + [ "-I" + self.context.fileName( "inc" ) ]
                    + [ "-I" + d for d in self.getIncludeDirectories() ],
                    context = self.context
                )

            def getFileName( self ):
                return self.__fileName

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
