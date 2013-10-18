import Artifacts
import Cpp


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(
            self,
            file=source
        )


class Script(Artifacts.AtomicArtifact):
    def __init__(self, source, packages):
        assert isinstance(source, Source)
        assert all(isinstance(p, (Module, CppModule, Package)) for p in packages)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=source.name[:-3],
            files=["bin/" + source.name[:-3]],
            strongDependencies=[source],
            orderOnlyDependencies=packages
        )
        self.run = None  # @todo


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
    def __init__(self, name, packages):
        assert all(isinstance(p, (Module, CppModule, Package)) for p in packages)
        Artifacts.CompoundArtifact.__init__(
            self,
            name=name,
            components=packages
        )


class CppModule(Artifacts.AtomicArtifact):
    def __init__(self, name, objects):
        assert all(isinstance(o, (Cpp.ObjectFile)) for o in objects)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=name,
            files=["pyc/" + name.replace(".", "/") + ".pyd"],
            strongDependencies=objects
        )
