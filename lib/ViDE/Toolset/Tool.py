from ViDE.Core.CallOnceAndCache import CallOnceAndCache

class Tool( CallOnceAndCache ):
    def __init__( self, version ):
        CallOnceAndCache.__init__( self )
        self.version = version

    def getFetchArtifact( self ):
        return self.getCached( "fetchArtifact", self.computeFetchArtifact )

    def getInstallArtifact( self ):
        return self.getCached( "installArtifact", self.__computeInstallArtifact )

    def __computeInstallArtifact( self ):
        # How do I ensure that the installArtifact depends on the fetchArtifact ?
        # Adding fetchArtifact as a dependency to installArtifact is not enough:
        # the *deepest* componants of installArtifact have to depend on fetchArtifact
        fetch = self.getFetchArtifact()
        return self.computeInstallArtifact()
