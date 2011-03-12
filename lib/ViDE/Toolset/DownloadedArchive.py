import urlparse
import os.path

import ViDE
from ViDE.Core.Artifact import AtomicArtifact
from ViDE.Core.Actions import DownloadFileAction

class DownloadedArchive( AtomicArtifact ):
    def __init__( self, url ):
        self.__url = url
        self.__file = os.path.join( ViDE.toolsCacheDirectory, os.path.basename( urlparse.urlparse( url ).path ) )
        AtomicArtifact.__init__(
            self,
            name = self.__file,
            files = [ self.__file ],
            strongDependencies = [],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = False
        )

    def doGetProductionAction( self ):
        return DownloadFileAction( self.__url, self.__file )
