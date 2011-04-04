class linux_gcc:
    def computeExecutableName( self, baseName ):
        return self.context.buildkit.fileName( "bin", baseName )

    def getDynamicLibraryFlag( self ):
        return "-shared"

    def computeDynamicLibraryName( self, baseName ):
        return self.context.buildkit.fileName( "lib", "lib" + baseName + ".so" )

    def getCppPythonModuleExtension( self ):
        return "so"

    def getSystemCompilationOptions( self ):
        return [ "-fPIC" ]
