import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class vs( ViDE.Buildkit.Buildkit ):
    class CPlusPlus:
        class Object( ViDE.Project.CPlusPlus.Object ):
            @staticmethod
            def computeName( buildkit, source, localLibraries ):
                return buildkit.fileName( "obj", source.getFileName() + ".obj" )

            def __init__( self, buildkit, source, localLibraries ):
                self.__buildkit = buildkit
                self.__fileName = self.__buildkit.fileName( "obj", source.getFileName() + ".obj" )
                ViDE.Project.CPlusPlus.Object.__init__( self, [ self.__fileName ], source, localLibraries )
        
            def doGetProductionAction( self ):
                sourceName = self.getSource().getFileName()
                return SystemAction(
                    [ "cl", "/c", sourceName ],
                    [ "/EHsc", "/I" + self.__buildkit.fileName( "inc" ), "/Fo" + self.__fileName ]
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
                ViDE.Project.Binary.Executable.__init__( self, name, [ self.__fileName ], objects, localLibraries )
                self.__localLibraries = localLibraries
                self.__objects = objects
            
            def doGetProductionAction( self ):
                return SystemAction(
                    [ "link", "/OUT:" + self.__fileName ],
                    [ o.getFileName() for o in self.__objects ]
                    + [ "/LIBPATH:" + self.__buildkit.fileName( "lib" ) ]
                    + [ lib.getLibName() + ".lib" for lib in self.__localLibraries ]
                )
