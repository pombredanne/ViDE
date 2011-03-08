class Tool:
    def __init__( self, version ):
        assert( version in self.getAvailableVersions() )
        self.version = version
