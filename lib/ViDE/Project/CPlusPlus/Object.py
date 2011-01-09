import os.path

from ViDE.Core.Actions import SystemAction

from ViDE.Project import Binary

class Object( Binary.Object ):
    def __init__( self, source, localLibraries ):
        self.__fileName = os.path.join( "build", "obj", source.getFileName() + ".o" )
        self.__source = source
        includes = self.parseAllIncludes()
        Binary.Object.__init__(
            self,
            name = self.__fileName,
            files = [ self.__fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [ lib.getCopiedHeaders() for lib in localLibraries ],
            automaticDependencies = includes,
            automatic = False
        )

    def doGetProductionAction( self ):
        return SystemAction( [ "g++", "-c", "-I" + os.path.join( "build", "inc" ), "-o" + self.__fileName, self.__source.getFileName() ], "g++ -c " + self.__source.getFileName() )

    def getFileName( self ):
        return self.__fileName

    def parseAllIncludes( self ):
        return []
        #depFile = DependencyFile( self.__source )
        #depFile.getProductionAction().execute()
        