from ViDE.Core.Descriptible import Descriptible

class BuildKit( Descriptible ):
    def __init__( self ):
        self.__cppCompiler = None
        self.__dynamicLibraryLinker = None

    def getCppCompiler( self ):
        return self.__cppCompiler
    
    def getDynamicLibraryLinker( self ):
        return self.__dynamicLibraryLinker
