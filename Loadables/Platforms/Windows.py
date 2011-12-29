import sys

from ViDE.Platform import Platform

class Windows( Platform ):
    def canBeDefault( self ):
        return sys.platform == "win32"

    def computeExecutableName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".exe" )

    def computeDynamicLibraryName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".dll" )

    def getDynamicLibraryLinkOptions( self ):
        return self.context.buildkit.getWindowsDynamicLibraryLinkOptions()

    def getCppPythonModuleExtension( self ):
        raise Exception( "Under Windows, Python modules cannot be built with gcc. Use Visual Studio." )
