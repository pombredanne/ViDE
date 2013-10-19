import unittest
import subprocess
import ActionTree
import MockMockMock

import Artifacts


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(
            self,
            file=source
        )

    def check(self):  # pragma no cover (@todo)
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


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()

    def tearDown(self):
        self.mocks.tearDown()

    def testBuild(self):
        a = ObjectFile(Source("foo.cpp"))._createBaseBuildAction()
        self.assertEqual(a.label, "g++ -c foo.cpp")
        co = self.mocks.replace("subprocess.check_output")
        cc = self.mocks.replace("subprocess.check_call")
        co.expect(["python-config", "--includes"]).andReturn("-I/bar -I/baz\n")
        cc.expect(["g++", "-c", "foo.cpp", "-o", "obj/foo.cpp.o", "-fPIC", "-I/bar", "-I/baz"])
        a.execute()


if __name__ == "__main__":
    unittest.main()
