from ViDE.Core.CallOnceAndCache import CallOnceAndCache

class Tool( CallOnceAndCache ):
    def __init__( self, version ):
        CallOnceAndCache.__init__( self )
        self.version = version

    def getInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return self.getCached( "installArtifact", self.computeInstallArtifact, context, downloadOnly, strongDependencies )
