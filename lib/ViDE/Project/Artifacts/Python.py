import unittest
import py_compile
import re
import os
import shutil
import subprocess
import ActionTree
import MockMockMock

import Artifacts
import Cpp


class Source(Artifacts.InputArtifact):
    def __init__(self, source):
        assert isinstance(source, (str, unicode))
        Artifacts.InputArtifact.__init__(
            self,
            file=source
        )

    def check(self):  # pragma no cover (@todo)
        # @todo What other tools could be used? PyLint, and?
        subprocess.check_call(["pep8"] + self.files)


class Script(Artifacts.AtomicArtifact):
    def __init__(self, source, packages):
        assert isinstance(source, Source)
        assert all(isinstance(p, (Module, CppModule, Package)) for p in packages)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=source.name[:-3],
            files=["bin/" + os.path.basename(source.name)[:-3]],
            strongDependencies=[source],
            orderOnlyDependencies=packages
        )
        self.source = source

    def run(self, arguments):  # pragma no cover (@todo)
        os.environ["PYTHONPATH"] = "pyc"
        subprocess.check_call([self.files[0]] + arguments)
        del os.environ["PYTHONPATH"]

    def _createBaseBuildAction(self):
        return ActionTree.Action(self.__build, "cp " + self.source.name + " " + self.files[0])

    def __build(self):
        shutil.copyfile(self.source.name, self.files[0])
        os.chmod(self.files[0], 0775)


class Module(Artifacts.AtomicArtifact):
    def __init__(self, source, strip):
        assert isinstance(source, Source)
        Artifacts.AtomicArtifact.__init__(
            self,
            name=strip(source.name)[:-3].replace("/", "."),
            files=["pyc/" + strip(source.name) + "c"],
            strongDependencies=[source]
        )
        self.source = source

    def _createBaseBuildAction(self):
        return ActionTree.Action(self.__build, "python -m py_compile " + self.source.name)

    def __build(self):
        py_compile.compile(self.source.name, self.files[0], doraise=True)


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
            files=["pyc/" + name.replace(".", "/") + ".so"],
            strongDependencies=objects
        )
        self.objects = objects

    def _createBaseBuildAction(self):
        return ActionTree.Action(self.__build, "g++ -o " + self.name)

    __spaces = re.compile(" +")

    def __build(self):
        pythonLibs = CppModule.__spaces.split(subprocess.check_output(["python-config", "--libs"]).strip())
        subprocess.check_call(["g++", "-shared", "-o", self.files[0]] + [o.name for o in self.objects] + ["-lboost_python"] + pythonLibs)


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.check_output = self.mocks.replace("subprocess.check_output")
        self.check_call = self.mocks.replace("subprocess.check_call")
        self.py_compile = self.mocks.replace("py_compile.compile")
        self.cp = self.mocks.replace("shutil.copyfile")
        self.chmod = self.mocks.replace("os.chmod")

    def tearDown(self):
        self.mocks.tearDown()

    def testBuildScript(self):
        a = Script(Source("foo/bar/baz.py"), [])._createBaseBuildAction()
        self.assertEqual(a.label, "cp foo/bar/baz.py bin/baz")
        self.cp.expect("foo/bar/baz.py", "bin/baz")
        self.chmod.expect("bin/baz", 0775)
        a.execute()

    def testBuildModule(self):
        a = Module(Source("foo/bar/baz.py"), lambda s: s[4:])._createBaseBuildAction()
        self.assertEqual(a.label, "python -m py_compile foo/bar/baz.py")
        self.py_compile.expect("foo/bar/baz.py", "pyc/bar/baz.pyc", doraise=True)
        a.execute()

    def testBuildCppModule(self):
        a = CppModule("bar.foo", [Cpp.ObjectFile(Cpp.Source("foo.cpp"))])._createBaseBuildAction()
        self.assertEqual(a.label, "g++ -o bar.foo")
        self.check_output.expect(["python-config", "--libs"]).andReturn("-lbar -lbaz\n")
        self.check_call.expect(["g++", "-shared", "-o", "pyc/bar/foo.so", "obj/foo.cpp.o", "-lboost_python", "-lbar", "-lbaz"])
        a.execute()


if __name__ == "__main__":
    unittest.main()
