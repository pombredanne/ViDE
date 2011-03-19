class linux_gcc:
    def computeExecutableName( self, context, baseName ):
        return context.buildkit.fileName( "bin", baseName )

    def getDynamicLibraryFlag( self ):
        return "-shared"

    def computeDynamicLibraryName( self, context, baseName ):
        return context.buildkit.fileName( "lib", "lib" + baseName + ".so" )
