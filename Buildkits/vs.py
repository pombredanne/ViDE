import os

import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction

class CPlusPlus:
    class Object( ViDE.Project.CPlusPlus.Object ):
        def __init__( self, source, localLibraries ):
            self.__fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
            ViDE.Project.CPlusPlus.Object.__init__( self, [ self.__fileName ], source, localLibraries )
    
        def doGetProductionAction( self ):
            sourceName = self.getSource().getFileName()
            return SystemAction(
                [ "cl", "/c", sourceName ]
                + [ "/I" + os.path.join( "build", "inc" ), "/Fo" + self.__fileName ],
                "cl " + sourceName
            )
    
        def getFileName( self ):
            return self.__fileName

class Binary:
    class Executable( ViDE.Project.Binary.Executable ):
        def __init__( self, name, objects, localLibraries ):
            self.__fileName = os.path.join( "build", "bin", name + ".exe" )
            ViDE.Project.Binary.Executable.__init__( self, name, [ self.__fileName ], objects, localLibraries )
            self.__localLibraries = localLibraries
            self.__objects = objects
        
        def doGetProductionAction( self ):
            return SystemAction(
                [ "link", "/OUT:" + self.__fileName ]
                + [ o.getFileName() for o in self.__objects ]
                + [ "/LIBPATH:" + os.path.join( "build", "lib" ) ]
                + [ lib.getLibName() + ".lib" for lib in self.__localLibraries ],
                "link /OUT:" + self.__fileName
            )
