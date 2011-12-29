import sys

from ViDE.Flavour import Flavour

class Debug( Flavour ):
    def canBeDefault( self ):
        return True

    def getCompilationOptions( self ):
        return self.context.buildkit.getDebugCompilationOptions()

    def getLinkOptions( self ):
        return self.context.buildkit.getDebugLinkOptions()
