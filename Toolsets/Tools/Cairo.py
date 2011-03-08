from ViDE.Core.Artifact import CompoundArtifact
from ViDE.Toolset import Tool, DownloadedArchive

class Cairo( Tool ):
    availableVersions = {
        "scm": None,
        "1.10.2": ( "0.20.2" )
    }

    @staticmethod
    def getAvailableVersions():
        return Cairo.availableVersions.keys()
    
    def getToolDependencies( self ):
        return []

    def getFetchArtifact( self ):
        if self.version == "scm":
            return blah
        else:
            cairoVersion = self.version
            pixmanVersion = Cairo.availableVersions[ self.version ]
            return CompoundArtifact(
                name = "packages",
                componants = [
                    DownloadedArchive( "http://www.cairographics.org/releases/cairo-" + cairoVersion + ".tar.gz" ),
                    DownloadedArchive( "http://www.cairographics.org/releases/pixman-" + pixmanVersion + ".tar.gz" )
                ],
                explicit = False
            )

    def getInstallArtifact( self ):
        if self.version == "scm":
            return blih
        else:
            return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )

class Cairomm( Tool ):
    def getToolDependencies( self ):
        return [ ( Cairo, Either( Interval( "1.15", "1.19" ), Set( "scm", "scm-stable" ) ) ) ]
