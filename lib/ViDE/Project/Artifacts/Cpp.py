import Artifacts


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(self, source, [source])


class ObjectFile(Artifacts.AtomicArtifact):
    def __init__(self, source):
        assert isinstance(source, Source)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=source.name + ".o",
            files=[source.name + ".o"],
            strongDependencies=[source]
        )
        self.source = source
