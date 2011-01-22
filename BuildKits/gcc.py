import os

import ViDE.Project.CPlusPlus.Object
from ViDE.Core.Actions import SystemAction

class CPlusPlus:
    class Object( ViDE.Project.CPlusPlus.Object ):
        def __init__( self, source, localLibraries ):
            self.__fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
            ViDE.Project.CPlusPlus.Object.__init__( self, [ self.__fileName ], source, localLibraries )
    
        def doGetProductionAction( self ):
            sourceName = self.getSource().getFileName()
            return SystemAction( [ "g++", "-c", "-I" + os.path.join( "build", "inc" ), "-o" + self.__fileName, sourceName ], "g++ -c " + sourceName )
    
        def getFileName( self ):
            return self.__fileName
