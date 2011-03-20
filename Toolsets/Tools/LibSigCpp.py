from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

class LibSigCpp( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "libsigc++",
            archiveUrl = "http://ftp.gnome.org/pub/GNOME/sources/libsigc++/" + ".".join( self.version.split( "." )[:-1] ) + "/libsigc++-" + self.version + ".tar.bz2",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []
