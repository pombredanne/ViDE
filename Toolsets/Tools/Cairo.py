from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadedArchive, UnarchiveConfigureMakeMakeinstall

class Pixman( Tool ):
    def computeFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/pixman-" + self.version + ".tar.gz" )

    def computeInstallArtifact( self, strongDependencies ):
        return UnarchiveConfigureMakeMakeinstall(
            archive = "pixman-" + self.version + ".tar.gz",
            file = "libpixman.so",
            strongDependencies = strongDependencies,
            configureOptions = [ "--whit-shared" ]
        )

class Cairo( Tool ):
    def computeFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/cairo-" + self.version + ".tar.gz" )

    def computeInstallArtifact( self, strongDependencies ):
        return UnarchiveConfigureMakeMakeinstall(
            archive = "cairo-" + self.version + ".tar.gz",
            file = "libcairo.so",
            strongDependencies = strongDependencies,
            configureOptions = [ "--whit-shared" ]
        )

class Cairomm( Tool ):
    def computeFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/cairomm-" + self.version + ".tar.gz" )

    def computeInstallArtifact( self, strongDependencies ):
        return UnarchiveConfigureMakeMakeinstall(
            archive = "cairomm-" + self.version + ".tar.gz",
            file = "libcairomm.so",
            strongDependencies = strongDependencies,
            configureOptions = [ "--whit-shared" ]
        )

class PyCairo( Tool ):
    def computeFetchArtifact( self ):
        # Python 2
        return DownloadedArchive( "http://www.cairographics.org/releases/py2cairo-" + self.version + ".tar.gz" )
        # Python 3
        # return DownloadedArchive( "http://www.cairographics.org/releases/pycairo-" + self.version + ".tar.bz2" )

    def computeInstallArtifact( self, strongDependencies ):
        return UnarchiveConfigureMakeMakeinstall(
            archive = "py2cairo-" + self.version + ".tar.gz",
            file = "pycairo",
            strongDependencies = strongDependencies,
            configureOptions = [ "--whit-shared" ]
        )
