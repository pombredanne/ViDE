import sys

from ViDE.Platform import Platform

class Linux( Platform ):
    def canBeDefault( self ):
        return sys.platform == "linux2"

    def computeExecutableName( self, baseName ):
        return self.context.fileName( "bin", baseName )

    def computeDynamicLibraryName( self, baseName ):
        return self.context.fileName( "lib", "lib" + baseName + ".so" )

    def getDynamicLibraryLinkOptions( self ):
        return self.context.buildkit.getLinuxDynamicLibraryLinkOptions()

    def getCppPythonModuleExtension( self ):
        return "so"
