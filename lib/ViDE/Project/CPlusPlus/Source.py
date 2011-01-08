from ViDE.Core.Artifact import InputArtifact

class Source( InputArtifact ):
    def __init__( self, fileName ):
        InputArtifact.__init__( self, name = fileName, files = [ fileName ], automatic = False )
        self.__fileName = fileName
        
    def getFileName( self ):
        return self.__fileName
