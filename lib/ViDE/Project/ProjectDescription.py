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
        return ProjectDescription(self.name, self.__extractTopLevelArtifacts())

    def __extractTopLevelArtifacts(self):
        artifactsToWalk = set(self.artifacts)
        allArtifacts = set()
        while len(artifactsToWalk) != 0:
            artifact = artifactsToWalk.pop()
            allArtifacts.add(artifact)
            for a in artifact.getLinkedArtifacts():
                artifactsToWalk.add(a)

        topLevelArtifacts = set(allArtifacts)
        artifactsToWalk = allArtifacts
        while len(artifactsToWalk) != 0:
            artifact = artifactsToWalk.pop()
            for a in artifact.getContainedArtifacts():
                artifactsToWalk.add(a)
                topLevelArtifacts.discard(a)

        return list(topLevelArtifacts)


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


class ProjectBuildingTestCase(unittest.TestCase):
    def testBuildProjectWithImplicitDependencies(self):
        builder = ProjectBuilder()
        x = builder.createArtifact(Artifacts.Artifacts.SubatomicArtifact, "x", ["a"])
        a = Artifacts.Artifacts.AtomicArtifact("a", ["a"], [], [], [x])
        b = Artifacts.Artifacts.AtomicArtifact("b", ["b"])
        c = Artifacts.Artifacts.AtomicArtifact("c", ["c"], [a], [b])
        d = builder.createArtifact(Artifacts.Artifacts.AtomicArtifact, "d", ["d"], [c])
        p = builder.createProject()
        self.assertEqual(len(p.artifacts), 4)
        self.assertIn(a, p.artifacts)
        self.assertIn(b, p.artifacts)
        self.assertIn(c, p.artifacts)
        self.assertIn(d, p.artifacts)

    def testBuildProjectWithExplicitComponents(self):
        builder = ProjectBuilder()
        a = builder.createArtifact(Artifacts.Artifacts.AtomicArtifact, "a", ["a"])
        b = builder.createArtifact(Artifacts.Artifacts.CompoundArtifact, "b", [a])
        c = builder.createArtifact(Artifacts.Artifacts.CompoundArtifact, "c", [b])
        p = builder.createProject()
        self.assertEqual(len(p.artifacts), 1)
        self.assertIn(c, p.artifacts)


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
                packages=[b1, b3],
                strip=lambda f: f[5:]
            )

            PythonScript(
                source="hello.py"
            )
        """))
        self.assertEqual(
            sorted(a.name for a in p.artifacts),
            [
                "a",
                "a.py",
                "b",
                "b3.cpp",
                "hello",
                "hello.py",
                "obj/b3.cpp.o",
                "pack/b/__init__.py",
                "pack/b/b1.py",
            ]
        )

    def testLoadProjectDescriptionWithTestingArtifacts(self):
        p = fromString(textwrap.dedent("""\
            bar = PythonSource("bar.py")

            UnitTest(PythonScript(
                source="hello.py",
                packages=["foo.py", bar]
            ))
        """))
        self.assertEqual(
            sorted(a.name for a in p.artifacts),
            [
                "bar",
                "bar.py",
                "foo",
                "foo.py",
                "hello",
                "hello.py",
                "tst/hello.ok",
            ]
        )


if __name__ == "__main__":
    unittest.main()
