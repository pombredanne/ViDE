from ViDE.Project.BasicArtifacts import MonofileInputArtifact, CopiedArtifact

class Source( MonofileInputArtifact ):
    pass

class Script( CopiedArtifact ):
    def __init__( self, buildkit, source, strip, explicit ):
         CopiedArtifact.__init__(
            self,
            buildkit,
            source = source,
            destination = buildkit.fileName( "bin", strip( source.getFileName() ) ),
            explicit = explicit
        )

# class Module( AtomicArtifact ):
    # pass

# class Package( CompoundArtifact ):
    # pass
        
# class CModule:
    # pass
