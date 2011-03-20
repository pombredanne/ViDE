from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact, AtomicArtifact

class Source( MonofileInputArtifact ):
    pass

class Object( AtomicArtifact ):
    def __init__( self, context, files, source, explicit ):
        AtomicArtifact.__init__(
            self,
            context = context,
            name = files[ 0 ],
            files = files,
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )
        self.__source = source

    def getSource( self ):
        return self.__source

    def getLibrariesToLink( self ):
        return []
