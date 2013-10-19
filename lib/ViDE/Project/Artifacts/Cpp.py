import subprocess
import ActionTree

import Artifacts


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(
            self,
            file=source
        )

    def check(self):
        # @todo Implement static code analysis for C/C++, use at least lint
        pass


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

    def _createBaseBuildAction(self):
        return ActionTree.Action(self.__build, "g++ -c " + self.source.name)

    def __build(self):
        pythonIncludes = subprocess.check_output(["python-config", "--includes"]).strip().split(" ")
        subprocess.check_call(["g++", "-c", self.source.name, "-o", self.name, "-fPIC"] + pythonIncludes)
