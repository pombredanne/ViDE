import os.path

from ViDE.Core.Actions import SystemAction

from ViDE.Project import Binary

class Object( Binary.Object ):
    def __init__( self, source ):
        fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
        Binary.Object.__init__(
            self,
            name = fileName,
            files = [ fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automatic = False
        )
        self.__fileName = fileName
        self.__source = source

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-c", "-o" + self.__fileName, self.__source.getFileName() ], "g++ -c " + self.__source.getFileName() )

    def getFileName( self ):
        return self.__fileName
