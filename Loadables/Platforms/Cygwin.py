import sys

from ViDE.Platform import Platform

class Cygwin( Platform ):
    def canBeDefault( self ):
        return sys.platform == "cygwin"

    def computeExecutableName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".exe" )
