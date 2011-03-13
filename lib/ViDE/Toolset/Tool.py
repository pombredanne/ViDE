from ViDE.Core.CallOnceAndCache import CallOnceAndCache

class Tool( CallOnceAndCache ):
    def __init__( self, version ):
        CallOnceAndCache.__init__( self )
        self.version = version

    def getInstallArtifact( self, toolset, downloadOnly, strongDependencies ):
        return self.getCached( "installArtifact", self.computeInstallArtifact, toolset, downloadOnly, strongDependencies )
