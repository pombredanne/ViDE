import ViDE
from ViDE.Platform import Platform

class Cygwin( Platform ):
    def canBeDefault( self ):
        return ViDE.host() == "cygwin"

    def computeExecutableName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".exe" )

    def computeDynamicLibraryName( self, baseName ):
        return self.context.fileName( "bin", baseName + ".dll" )

    def getDynamicLibraryLinkOptions( self ):
        return self.context.buildkit.getCygwinDynamicLibraryLinkOptions()

    def getCppPythonModuleExtension( self ):
        return "dll"
