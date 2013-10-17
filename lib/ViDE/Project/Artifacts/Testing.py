import Artifacts


class UnitTest(Artifacts.AtomicArtifact):
    def __init__(self, executable, *arguments):
        assert hasattr(executable, "run")
        assert all(isinstance(a, (str, unicode)) for a in arguments)
        marker = "tst/" + executable.name + "".join("_" + a for a in arguments) + ".ok"
        Artifacts.AtomicArtifact.__init__(
            self,
            name=marker,
            files=[marker],
            strongDependencies=[executable] + executable.orderOnlyDependencies
        )
