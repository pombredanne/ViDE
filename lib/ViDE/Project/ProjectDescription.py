# -*- coding: utf-8 -*-

import unittest
import textwrap

import Artifacts


class ProjectDescription:
    def __init__(self, name, artifacts):
        self.name = name
        self.artifacts = artifacts


class ProjectBuilder:
    def __init__(self):
        self.name = None
        self.artifacts = []

    def describeProject(self, name):
        self.name = name

    def createArtifact(self, factory, *a, **k):
        artifact = factory(*a, **k)
        self.artifacts.append(artifact)
        return artifact

    def __createArtifact(self, factory):
        return lambda *a, **k: self.createArtifact(factory, *a, **k)

    def parseString(self, s):
        d = {"Project": self.describeProject}
        for factory in Artifacts.allFactories:
            d[factory.__name__] = self.__createArtifact(factory)
        exec s in d

    def createProject(self):
        return ProjectDescription(self.name, self.artifacts)


def fromString(s):
    b = ProjectBuilder()
    b.parseString(s)
    return b.createProject()


class EvalExecTestCase(unittest.TestCase):
    def testEvalIsLimitedToExpressions(self):
        self.assertEqual(eval("40 + 2"), 42)

    def testExecPolutesDir(self):
        self.assertNotIn("a", dir())
        exec "import os\na=42"
        self.assertIn("a", dir())
        self.assertIn("os", dir())

    def testExecInCustomDict(self):
        d = {"f": lambda x: 2 * x}
        exec "import os\na=f(21)" in d
        self.assertNotIn("a", dir())
        self.assertNotIn("os", dir())
        self.assertIn("a", d)
        self.assertEqual(d["a"], 42)
        self.assertIn("os", d)


class ProjectLoadingTestCase(unittest.TestCase):
    def testLoadSimplestProjectDescription(self):
        p = fromString(textwrap.dedent("""\
            Project(
                name="Project name"
            )
        """))
        self.assertEqual(p.name, "Project name")
        self.assertEqual(len(p.artifacts), 0)

    def testLoadProjectDescriptionWithPythonArtifacts(self):
        p = fromString(textwrap.dedent("""\
            Project(
                name="Project name"
            )

            PythonModule(
                source="a.py"
            )

            b1 = PythonModule(
                source="pack/b/b1.py",
                strip=lambda f: f[5:]
            )

            b3 = CppPythonModule(
                name="b.b3",
                sources=["b3.cpp"],
                localLibraries=[]
            )

            PythonPackage(
                name="b",
                sources=[PythonSource("pack/b/__init__.py"), "pack/b/b2.py"],
                modules=[b1, b3],
                strip=lambda f: f[5:]
            )

            PythonScript(
                source="hello.py"
            )
        """))
        self.assertEqual(p.name, "Project name")
        self.assertEqual(len(p.artifacts), 6)


if __name__ == "__main__":
    unittest.main()
