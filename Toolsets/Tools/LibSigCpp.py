from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class LibSigCpp( Tool ):
    def computeInstallArtifact( self, toolset, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            toolset = toolset,
            downloadOnly = downloadOnly,
            toolName = "libsigc++",
            archiveUrl = "http://ftp.gnome.org/pub/GNOME/sources/libsigc++/" + ".".join( self.version.split( "." )[:-1] ) + "/libsigc++-" + self.version + ".tar.bz2",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []
