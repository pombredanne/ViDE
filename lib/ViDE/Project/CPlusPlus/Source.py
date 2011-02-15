from ViDE.Core.Artifact import InputArtifact

class MonofileInputArtifact( InputArtifact ):
    @staticmethod
    def computeName( buildkit, fileName ):
        return fileName

    def __init__( self, buildkit, fileName ):
        InputArtifact.__init__( self, name = fileName, files = [ fileName ] )
        self.__fileName = fileName
        
    def getFileName( self ):
        return self.__fileName

class Header( MonofileInputArtifact ):
    pass

class Source( MonofileInputArtifact ):
    pass

