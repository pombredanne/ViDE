import Artifacts


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(self, source, [source])


class Script:
    def __init__(self, source):
        assert isinstance(source, Source)


class Module(Artifacts.AtomicArtifact):
    def __init__(self, source, strip):
        assert isinstance(source, Source)
        Artifacts.AtomicArtifact.__init__(self, source.name + "c", [source.name + "c"], [source], [])


class Package(Artifacts.CompoundArtifact):
    def __init__(self, name, modules):
        assert isinstance(name, (str, unicode))
        assert all(isinstance(module, (Module, CModule)) for module in modules)
        Artifacts.CompoundArtifact.__init__(self, name, modules)


class CModule:
    def __init__(self, *a, **k):
        pass
