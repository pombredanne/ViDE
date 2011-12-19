from ViDE.Toolset import Tool

class Gdi( Tool ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return "gdi32"
