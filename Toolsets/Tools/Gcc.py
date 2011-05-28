from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

# ftp://ftp.gnu.org/gnu/gcc/gcc-4.6.0/gcc-4.6.0.tar.bz2
# http://www.mpfr.org/mpfr-current/mpfr-3.0.0.tar.bz2
# http://www.multiprecision.org/mpc/download/mpc-0.9.tar.gz

class Gcc( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "gcc",
            #archiveUrl = "ftp://ftp.gnu.org/gnu/make/make-" + self.version + ".tar.bz2",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []

