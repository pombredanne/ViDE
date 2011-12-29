from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class PkgConfig( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "pkgconfig",
            archiveUrl = "http://pkgconfig.freedesktop.org/releases/pkg-config-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []
