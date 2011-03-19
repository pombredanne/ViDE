from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadUnarchiveConfigureMakeMakeinstall

from PkgConfig import PkgConfig
from LibSigCpp import LibSigCpp

class Pixman( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "pixman",
            archiveUrl = "http://www.cairographics.org/releases/pixman-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []

class LibPng( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "libpng",
            archiveUrl = "ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []

class FreeType( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "freetype",
            archiveUrl = "http://download.savannah.gnu.org/releases/freetype/freetype-" + self.version + ".tar.bz2",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return []

class FontConfig( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "fontconfig",
            archiveUrl = "http://www.freedesktop.org/software/fontconfig/release/fontconfig-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return [ FreeType ]

class Cairo( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "cairo",
            archiveUrl = "http://www.cairographics.org/releases/cairo-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return [ Pixman, PkgConfig, LibPng, FontConfig ]

class Cairomm( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "cairomm",
            archiveUrl = "http://www.cairographics.org/releases/cairomm-" + self.version + ".tar.gz",
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return [ Cairo, LibSigCpp ]

class PyCairo( Tool ):
    def computeInstallArtifact( self, context, downloadOnly, strongDependencies ):
        return DownloadUnarchiveConfigureMakeMakeinstall(
            context = context,
            downloadOnly = downloadOnly,
            toolName = "pycairo",
            archiveUrl = "http://www.cairographics.org/releases/py2cairo-" + self.version + ".tar.gz", # Python 2
            # archiveUrl = "http://www.cairographics.org/releases/pycairo-" + self.version + ".tar.bz2", # Python 3
            strongDependencies = strongDependencies
        )

    def getDependencies( self ):
        return [ Cairo ]
