import os.path

from ViDE.Core.Artifact import AtomicArtifact

class Executable( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries ):
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [ lib.getBinary() for lib in localLibraries ],
            automaticDependencies = []
        )
