from ViDE.Core.Descriptible import Descriptible

class BuildKit( Descriptible ):
    def __init__( self ):
        self.__compiler = None

    def setCompiler( self, compiler ):
        self.__compiler = compiler

    def getCompiler( self ):
        return self.__compiler
