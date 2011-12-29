import sys

from ViDE.Flavour import Flavour

class Test( Flavour ):
    def canBeDefault( self ):
        return False

    def getCompilationOptions( self ):
        return self.context.buildkit.getTestCompilationOptions()

    def getLinkOptions( self ):
        return self.context.buildkit.getTestLinkOptions()
