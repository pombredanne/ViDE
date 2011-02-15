import os

import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction

class gcc:
    class CPlusPlus:
        class Object( ViDE.Project.CPlusPlus.Object ):
            def __init__( self, source, localLibraries ):
                self.__fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
                ViDE.Project.CPlusPlus.Object.__init__( self, [ self.__fileName ], source, localLibraries )
        
            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "g++", "-c", sourceName ],
                    [ "-I" + os.path.join( "build", "inc" ), "-o" + self.__fileName ]
                )
        
            def getFileName( self ):
                return self.__fileName

    class Binary:
        class Executable( ViDE.Project.Binary.Executable ):
            def __init__( self, name, objects, localLibraries ):
                self.__fileName = os.path.join( "build", "bin", name )
                ViDE.Project.Binary.Executable.__init__( self, name, [ self.__fileName ], objects, localLibraries )
                self.__localLibraries = localLibraries
                self.__objects = objects
            
            def doGetProductionAction( self ):
                return SystemAction(
                    [ "g++", "-o" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "-L" + os.path.join( "build", "lib" ) ]
                    + [ "-l" + lib.getLibName() for lib in self.__localLibraries ]
                )

        class DynamicLibraryBinary( ViDE.Project.Binary.DynamicLibraryBinary ):
            def __init__( self, name, objects ):
                self.__fileName = os.path.join( "build", "lib", name + ".dll" )
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
