from ViDE.Core.Artifact import InputArtifact

class MonofileInputArtifact( InputArtifact ):
    @staticmethod
    def computeName( buildkit, fileName, explicit ):
        return fileName

    def __init__( self, buildkit, fileName, explicit ):
        InputArtifact.__init__( self, name = fileName, files = [ fileName ], explicit = explicit )
        self.__fileName = fileName
        
    def getFileName( self ):
        return self.__fileName

class Header( MonofileInputArtifact ):
    pass

class Source( MonofileInputArtifact ):
    pass

