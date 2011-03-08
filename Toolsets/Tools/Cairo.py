from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadedArchive, UnarchiveConfigureMakeMakeinstall

class Pixman( Tool ):
    def getFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/pixman-" + self.version + ".tar.gz" )

    def getInstallArtifact( self ):
        return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )

class Cairo( Tool ):
    def getFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/cairo-" + self.version + ".tar.gz" )

    def getInstallArtifact( self ):
        return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )

class Cairomm( Tool ):
    def getFetchArtifact( self ):
        return DownloadedArchive( "http://www.cairographics.org/releases/cairomm-" + self.version + ".tar.gz" )

    def getInstallArtifact( self ):
        return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )

class PyCairo( Tool ):
    def getFetchArtifact( self ):
        # Python 2
        return DownloadedArchive( "http://www.cairographics.org/releases/py2cairo-" + self.version + ".tar.gz" )
        # Python 3
        # return DownloadedArchive( "http://www.cairographics.org/releases/pycairo-" + self.version + ".tar.bz2" )

    def getInstallArtifact( self ):
        return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )
