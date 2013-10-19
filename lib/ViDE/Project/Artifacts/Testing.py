import unittest
import subprocess
import ActionTree
import MockMockMock

import Artifacts


class UnitTest(Artifacts.AtomicArtifact):
    _open = open  # Allow static dependency injection. But keep it private.

    def __init__(self, executable, arguments):
        assert hasattr(executable, "run")
        assert all(isinstance(a, (str, unicode)) for a in arguments)
        marker = "tst/" + executable.name + "".join("_" + a for a in arguments) + ".ok"
        Artifacts.AtomicArtifact.__init__(
            self,
            name=marker,
            files=[marker],
            strongDependencies=[executable] + executable.orderOnlyDependencies,
            orderOnlyDependencies=[],
            subatomicArtifacts=[]
        )
        self.executable = executable
        self.arguments = list(arguments)

    def _createBaseBuildAction(self):
        return ActionTree.Action(self.__build, self.executable.name + ' "' + '" "'.join(self.arguments) + '"')

    def __build(self):
        self.executable.run(self.arguments)
        self._open(self.files[0], "w").close()


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.open = self.mocks.replace("UnitTest._open")
        self.run = self.mocks.create("run")
        self.file = self.mocks.create("file")

    def tearDown(self):
        self.mocks.tearDown()

    def testBuildUnitTest(self):
        class Script:
            def __init__(this, name, run):
                this.name = name
                this.orderOnlyDependencies = []
                this.run = run

        script = Script("scripteuh", self.run.object)
        self.run.expect(["foo", "bar"])
        self.open.expect("tst/scripteuh_foo_bar.ok", "w").andReturn(self.file.object)
        self.file.expect.close()

        a = UnitTest(script, ["foo", "bar"])._createBaseBuildAction()
        self.assertEqual(a.label, 'scripteuh "foo" "bar"')
        a.execute()


if __name__ == "__main__":
    unittest.main()
