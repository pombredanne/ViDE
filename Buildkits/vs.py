import ViDE.Project.CPlusPlus.Object
import ViDE.Project.Binary.Executable
from ViDE.Core.Actions import SystemAction
import ViDE.Buildkit

class CPlusPlusObject( ViDE.Project.CPlusPlus.Object ):
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

class BinaryExecutable( ViDE.Project.Binary.Executable ):
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

class CPlusPlusFactory:
    def __init__( self, buildkit ):
        self.__buildkit = buildkit

    def Object( self, *args ):
        return CPlusPlusObject( self.__buildkit, *args )

class BinaryFactory:
    def __init__( self, buildkit ):
        self.__buildkit = buildkit

    def Executable( self, *args ):
        return BinaryExecutable( self.__buildkit, *args )

class vs( ViDE.Buildkit.Buildkit ):
    def __init__( self, name ):
        ViDE.Buildkit.Buildkit.__init__( self, name )
        self.CPlusPlus = CPlusPlusFactory( self )
        self.Binary = BinaryFactory( self )
