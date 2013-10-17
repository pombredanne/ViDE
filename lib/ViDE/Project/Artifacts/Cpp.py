import Artifacts


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(self, source, [source])


class ObjectFile(Artifacts.AtomicArtifact):
    def __init__(self, source):
        assert isinstance(source, Source)
        obj = "obj/" + source.name + ".o"
        Artifacts.AtomicArtifact.__init__(
            self,
            name=obj,
            files=[obj],
            strongDependencies=[source]
        )
        self.source = source
