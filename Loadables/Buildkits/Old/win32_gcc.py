class win32_gcc:
    def computeExecutableName( self, baseName ):
        return self.context.buildkit.fileName( "bin", baseName + ".exe" )

    def getDynamicLibraryFlag( self ):
        return "-shared"

    def computeDynamicLibraryName( self, baseName ):
        return self.context.buildkit.fileName( "lib", baseName + ".dll" )

    def getCppPythonModuleExtension( self ):
        raise Exception( "Under Windows, Python modules cannot be built with gcc. Use Visual Studio." )

    def getSystemCompilationOptions( self ):
        return []
