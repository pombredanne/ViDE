import sys

from ViDE.Platform import Platform

class Windows( Platform ):
    def canBeDefault( self ):
        return sys.platform == "win32"

    def computeExecutableName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".exe" )
