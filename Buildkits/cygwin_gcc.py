class cygwin_gcc:
    def computeExecutableName( self, context, baseName ):
        return context.buildkit.fileName( "bin", baseName + ".exe" )

    def getDynamicLibraryFlag( self ):
        return "-shared"

    def computeDynamicLibraryName( self, context, baseName ):
        return context.buildkit.fileName( "lib", baseName + ".dll" )
