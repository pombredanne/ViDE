import os.path

from ViDE.Core.Artifact import AtomicArtifact

class Executable( AtomicArtifact ):
    def __init__( self, buildkit, name, files, objects, localLibraries ):
        self.__localLibraries = localLibraries
        AtomicArtifact.__init__(
            self,
            name = name,
            files = files,
            strongDependencies = objects,
            orderOnlyDependencies = [ lib.getBinary() for lib in self.localLibrariesWithBinary() ],
            automaticDependencies = []
        )

    def localLibrariesWithBinary( self ):
        return [ lib for lib in self.__localLibraries if hasattr( lib, "getBinary" ) ]
