from ViDE.Core.CallOnceAndCache import CallOnceAndCache

class Tool( CallOnceAndCache ):
    def __init__( self, version ):
        CallOnceAndCache.__init__( self )
        self.version = version

    def getFetchArtifact( self ):
        return self.getCached( "fetchArtifact", self.computeFetchArtifact )

    def getInstallArtifact( self, toolset, previous ):
        return self.getCached( "installArtifact", self.computeInstallArtifact, toolset, previous )
