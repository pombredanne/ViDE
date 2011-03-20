class cygwin_gcc:
    def computeExecutableName( self, baseName ):
        return self.context.buildkit.fileName( "bin", baseName + ".exe" )

    def getDynamicLibraryFlag( self ):
        return "-shared"

    def computeDynamicLibraryName( self, baseName ):
        return self.context.buildkit.fileName( "lib", baseName + ".dll" )

    def getSystemCompilationOptions( self ):
        return []
