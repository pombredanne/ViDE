class darwin_gcc:
    def computeExecutableName( self, baseName ):
        return self.context.buildkit.fileName( "bin", baseName )

    def getDynamicLibraryFlag( self ):
        return "-dynamiclib"

    def computeDynamicLibraryName( self, baseName ):
        return self.context.buildkit.fileName( "lib", "lib" + baseName + ".dylib" )

    def getSystemCompilationOptions( self ):
        return []
