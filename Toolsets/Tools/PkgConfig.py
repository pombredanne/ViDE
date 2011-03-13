from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class PkgConfig( Tool ):
    def computeInstallArtifact( self, toolset, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            toolset = toolset,
            downloadOnly = downloadOnly,
            toolName = "pkgconfig",
            archiveUrl = "http://pkgconfig.freedesktop.org/releases/pkg-config-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []
