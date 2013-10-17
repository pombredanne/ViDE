import Artifacts
import Cpp


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(
            self,
            name=source,
            files=[source]
        )


class Script(Artifacts.AtomicArtifact):
    def __init__(self, source):
        assert isinstance(source, Source)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=source.name,
            files=["bin/" + source.name],
            strongDependencies=[source]
        )


class Module(Artifacts.AtomicArtifact):
    def __init__(self, source, strip):
        assert isinstance(source, Source)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=strip(source.name)[:-3].replace("/", "."),
            files=["pyc/" + strip(source.name) + "c"],
            strongDependencies=[source]
        )


class Package(Artifacts.CompoundArtifact):
    def __init__(self, name, modules):
        assert all(isinstance(m, (Module, CppModule)) for m in modules)
        Artifacts.CompoundArtifact.__init__(
            self,
            name=name,
            components=modules
        )


class CppModule(Artifacts.AtomicArtifact):
    def __init__(self, name, objects):
        assert all(isinstance(o, (Cpp.ObjectFile)) for o in objects)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=name,
            files=[name + ".pyd"],
            strongDependencies=objects
        )
