from ViDE.Toolset import Tool

class Pcap( Tool ):
    def getDependencies( self ):
        return []

    def getIncludeDirectories( self, context ):
        return []

    def getLibPath( self ):
        return None

    def getLibName( self ):
        return "pcap"
