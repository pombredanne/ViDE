from ViDE.Toolset import Tool

class Cairo( Tool ):
    availableVersions = {
        "scm": None, 
        "1.18": ( "1", "18" ),
        "1.19" : ( "1", "19" )
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
            major, minor = Cairo.availableVersions[ self.version ]
            return CompoundArtifact(
                componants = [
                    DownloadedArchive( "http://cairo.org/download/pixman" + major + "_" + minor + ".tar.gz" ),
                    DownloadedArchive( "http://cairo.org/download/cairo" + major + "_" + minor + ".tar.gz" )
                ]
            )

    def getInstallArtifact( self ):
        if self.version == "scm":
            return blih
        else:
            return UnarchiveConfigureMakeMakeinstall( configureOptions = [ "--with-shared" ] )

class Cairomm( Tool ):
    def getToolDependencies( self ):
        return [ ( Cairo, Either( Interval( "1.15", "1.19" ), Set( "scm", "scm-stable" ) ) ) ]
