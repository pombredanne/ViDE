import sys

from ViDE.Flavour import Flavour

class Release( Flavour ):
    def canBeDefault( self ):
        return False

    def getCompilationOptions( self ):
        return self.context.buildkit.getReleaseCompilationOptions()

    def getLinkOptions( self ):
        return self.context.buildkit.getReleaseLinkOptions()
