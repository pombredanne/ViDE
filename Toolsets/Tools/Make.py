from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class Make( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "make",
            archiveUrl = "ftp://ftp.gnu.org/gnu/make/make-" + self.version + ".tar.bz2",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []

