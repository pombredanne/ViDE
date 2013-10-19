import unittest
import os.path
import sys
import ActionTree
import ActionTree.StockActions
import MockMockMock

import AnotherPyGraphvizAgain.Compounds as gv


class _MemoForGetAction:
    def __init__(self, assumeOld, assumeNew, create):
        self.__assumeOld = assumeOld
        self.__assumeNew = assumeNew
        self.__create = create
        self.__actionsForArtifact = dict()
        self.__actionsForDirectories = dict()

    def getOrCreateActionForArtifact(self, artifact):
        artifactId = id(artifact)
        if artifactId not in self.__actionsForArtifact:
            self.__actionsForArtifact[artifactId] = artifact._createAction(self)
        return self.__actionsForArtifact[artifactId]

    def getOrCreateActionForDirectory(self, directory):
        if directory not in self.__actionsForDirectories:
            self.__actionsForDirectories[directory] = ActionTree.StockActions.CreateDirectory(directory)
        return self.__actionsForDirectories[directory]

    def mustCreateAction(self, artifact):
        return artifact._mustBeProduced(self.__assumeOld, self.__assumeNew)

    def createBaseAction(self, artifact):
        return self.__create(artifact)


class _Artifact(object):
    def __init__(self, name):
        assert isinstance(name, (str, unicode))
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def identifier(self):
        return gv.makeId(self.__name)

    @staticmethod
    def _getFileModificationTime(f):
        return os.stat(f).st_mtime  # pragma no cover (mocked system call)

    @staticmethod
    def _fileExists(f):
        return os.path.exists(f)  # pragma no cover (mocked system call)

    def _getNewestFileModificationTime(self, assumeOld, assumeNew):
        return max(self.__getCombinedFileModificationTime(f, assumeOld, assumeNew) for f in self.files)

    def _getOldestFileModificationTime(self, assumeOld, assumeNew):
        return min(self.__getCombinedFileModificationTime(f, assumeOld, assumeNew) for f in self.files)

    @staticmethod
    def __getCombinedFileModificationTime(f, assumeOld, assumeNew):
        if f in assumeOld:
            return 0
        elif not _Artifact._fileExists(f):
            return 0
        elif f in assumeNew:
            return sys.maxint
        else:
            return _Artifact._getFileModificationTime(f)


class _ArtifactWithFiles(_Artifact):
    def _createGraphNodeAndLinks(self, memo):
        if len(self.files) == 1 and self.files[0] == self.name:
            node = gv.Node(self.identifier)
        else:
            node = gv.Cluster(self.identifier)
            node.set("style", "solid")
            for f in self.files:
                fileNode = gv.Node(gv.makeId(f))
                fileNode.set("label", f)
                node.add(fileNode)
        node.set("label", self.name)
        return node, []


class _ArtifactWithSeveralFiles(_ArtifactWithFiles):
    def __init__(self, name, files):
        _ArtifactWithFiles.__init__(self, name)
        assert len(files) > 0
        self.__files = set(files)

    @property
    def files(self):
        return sorted(self.__files)


class InputArtifact(_ArtifactWithFiles):
    """
    An artifact that never needs to be produced
    """

    def __init__(self, file):
        _ArtifactWithFiles.__init__(self, file)
        self.__file = file

    @property
    def files(self):
        return [self.__file]

    def getLinkedArtifacts(self):
        return []

    def getContainedArtifacts(self):
        return []

    def _mustBeProduced(self, assumeOld, assumeNew):
        return False


class AtomicArtifact(_ArtifactWithSeveralFiles):
    """
    An artifact that is produced by a single action.
    """

    def __init__(self, name, files,
                 strongDependencies=[],
                 orderOnlyDependencies=[],
                 subatomicArtifacts=[]):
        """
        :param: strongDependencies If a strong dependency is rebuilt,
        then the artifact must be rebuilt.

        :param: orderOnlyDependencies If an order-only dependency is absent,
        then it must be build before the artifact. But if an order-only
        dependency is rebuilt, the artifact doesn't need to be rebuilt.
        """
        _ArtifactWithSeveralFiles.__init__(self, name, files)
        self.__strongDependencies = strongDependencies
        self.__orderOnlyDependencies = orderOnlyDependencies
        self.__subs = subatomicArtifacts

    @property
    def orderOnlyDependencies(self):
        return self.__orderOnlyDependencies

    def _createGraphNodeAndLinks(self, memo):
        if (
            len(self.__subs) == 0
            and len(self.files) == 1
            and self.files[0] == self.name
        ):
            node = gv.Node(self.identifier)
        else:
            node = gv.Cluster(self.identifier)
            node.set("style", "solid")
            for sub in self.__subs:
                subNode = memo.getOrCreateNode(sub)
                subNode.set("style", "dashed")
                node.add(subNode)
            for f in self.files:
                fileNode = gv.Node(gv.makeId(f))
                fileNode.set("label", f)
                node.add(fileNode)
        node.set("label", self.name)

        links = []
        for d in self.__strongDependencies:
            links.append(gv.Link(node, memo.getOrCreateNode(d)))
        for d in self.__orderOnlyDependencies:
            link = gv.Link(node, memo.getOrCreateNode(d))
            link.set("style", "dashed")
            links.append(link)

        return node, links

    def getLinkedArtifacts(self):
        return self.__strongDependencies + self.__orderOnlyDependencies

    def getContainedArtifacts(self):
        return self.__subs

    def check(self):
        pass

    def _createAction(self, memo):
        a = memo.createBaseAction(self)
        for f in self.files:
            a.addDependency(memo.getOrCreateActionForDirectory(os.path.dirname(f)))
        for d in self.__strongDependencies + self.__orderOnlyDependencies:
            if memo.mustCreateAction(d):
                a.addDependency(memo.getOrCreateActionForArtifact(d))
        return a

    def _createBaseTouchAction(self):
        return ActionTree.StockActions.TouchFiles(self.files)

    def _mustBeProduced(self, assumeOld, assumeNew):
        oldestFileModificationTime = self._getOldestFileModificationTime(assumeOld, assumeNew)
        if oldestFileModificationTime == 0:
            return True
        for d in self.__strongDependencies:
            if d._mustBeProduced(assumeOld, assumeNew):
                return True
            if d._getNewestFileModificationTime(assumeOld, assumeNew) > oldestFileModificationTime:
                return True
        return False


class CompoundArtifact(_Artifact):
    """
    An artifact not produced by a single action,
    but by all the production actions of its components.
    """

    def __init__(self, name, components):
        _Artifact.__init__(self, name)
        assert len(components) > 0
        self.__components = components

    @property
    def files(self):
        allFiles = []
        for c in self.__components:
            allFiles += c.files
        return allFiles

    def _createGraphNodeAndLinks(self, memo):
        node = gv.Cluster(self.identifier)
        node.set("label", self.name)
        node.set("style", "solid")
        for component in self.__components:
            node.add(memo.getOrCreateNode(component))
        return node, []

    def getLinkedArtifacts(self):
        return []

    def getContainedArtifacts(self):
        return self.__components

    def check(self):
        for c in self.__components:
            c.check()

    def _createAction(self, memo):
        a = memo.createBaseAction(self)
        for c in self.__components:
            if memo.mustCreateAction(c):
                a.addDependency(memo.getOrCreateActionForArtifact(c))
        return a

    def _createBaseTouchAction(self):
        return ActionTree.StockActions.NullAction()

    def _createBaseBuildAction(self):
        return ActionTree.StockActions.NullAction()

    def _mustBeProduced(self, assumeOld, assumeNew):
        return any(c._mustBeProduced(assumeOld, assumeNew) for c in self.__components)


class SubatomicArtifact(_ArtifactWithSeveralFiles):
    """
    An artifact that is produced by the production action of its
    atomicArtifact, but is useful on its own, for example as a dependency.
    """

    def getLinkedArtifacts(self):
        return []

    def getContainedArtifacts(self):
        return []


def getGraphOfArtifacts(artifacts):
    class Memo:
        def __init__(self):
            self.__nodesById = {}
            self.links = []

        def getOrCreateNode(self, artifact):
            id_ = id(artifact)
            node = self.__nodesById.get(id_)
            if node is None:
                node, links = artifact._createGraphNodeAndLinks(self)
                self.links.extend(links)
                self.__nodesById[id_] = node
            return node

    graph = gv.Graph("artifacts")
    graph.set("ranksep", "1")
    graph.nodeAttr.set("shape", "box")
    memo = Memo()
    for artifact in artifacts:
        graph.add(memo.getOrCreateNode(artifact))
    for link in memo.links:
        graph.add(link)
    return graph


class GraphTestCase(unittest.TestCase):
    def expect(self, *expectedMidleOfDotString):
        expectedBeginOfDotString = (
            'digraph "artifacts" ' +
            '{compound="true";ranksep="1";node [shape="box"];'
        )
        expectedEndOfDotString = '}'

        graph = getGraphOfArtifacts(self.artifacts)
        fileName = os.path.join(os.path.dirname(__file__), self.__class__.__name__ + "." + self._testMethodName + ".png")
        graph.drawTo(fileName)

        dotString = graph.dotString()
        self.assertEqual(
            dotString[:len(expectedBeginOfDotString)],
            expectedBeginOfDotString
        )
        self.assertEqual(
            dotString[
                len(expectedBeginOfDotString):-len(expectedEndOfDotString)
            ],
            "".join(line.strip() for line in expectedMidleOfDotString)
        )
        self.assertEqual(
            dotString[-len(expectedEndOfDotString):],
            expectedEndOfDotString
        )

    def testInputArtifact(self):
        self.artifacts = [InputArtifact("input")]
        self.expect(
            'input[label="input"];'
        )

    def testSingleFileAtomicArtifact(self):
        self.artifacts = [AtomicArtifact("atomic", ["atomic"])]
        self.expect(
            'atomic[label="atomic"];'
        )

    def testMultiFilesAtomicArtifact(self):
        self.artifacts = [
            AtomicArtifact("atomic", ["atomic1", "atomic2"])
        ]
        self.expect(
            'subgraph cluster_atomic{',
            '  label="atomic";',
            '  style="solid";',
            '  atomic1[label="atomic1"];',
            '  atomic2[label="atomic2"];',
            '};'
        )

    def testAtomicArtifactWithDependencies_SingleFile(self):
        strong = AtomicArtifact("strong", ["strong"])
        order = AtomicArtifact("order", ["order"])
        atomic = AtomicArtifact("atomic", ["atomic"], [strong], [order])
        self.artifacts = [atomic, strong, order]
        self.expect(
            'atomic[label="atomic"];',
            'order[label="order"];',
            'strong[label="strong"];',
            'atomic->order[style="dashed"];',
            'atomic->strong;'
        )

    def testAtomicArtifactWithDependencies_MultiFiles(self):
        strong = AtomicArtifact("strong", ["strongX"])
        order = AtomicArtifact("order", ["orderX"])
        atomic = AtomicArtifact("atomic", ["atomicX"], [strong], [order])
        self.artifacts = [atomic, strong, order]
        self.expect(
            'subgraph cluster_atomic{',
            '  label="atomic";',
            '  style="solid";',
            '  atomicX[label="atomicX"];',
            '};',
            'subgraph cluster_order{',
            '  label="order";',
            '  style="solid";',
            '  orderX[label="orderX"];',
            '};',
            'subgraph cluster_strong{',
            '  label="strong";',
            '  style="solid";',
            '  strongX[label="strongX"];',
            '};',
            'atomicX->orderX',
            '  [lhead="cluster_order",ltail="cluster_atomic",style="dashed"];',
            'atomicX->strongX[lhead="cluster_strong",ltail="cluster_atomic"];'
        )

    def testCompoundArtifactWithoutDependencies(self):
        component1 = InputArtifact("component1")
        component2 = AtomicArtifact("component2", ["component2"])
        compound = CompoundArtifact("compound", [component1, component2])
        self.artifacts = [compound]
        self.expect(
            'subgraph cluster_compound{',
            '  label="compound";',
            '  style="solid";',
            '  component1[label="component1"];',
            '  component2[label="component2"];',
            '};'
        )

    def testCompoundArtifactWithDependencies(self):
        dependency = AtomicArtifact("dependency", ["dependencyX"])
        component = AtomicArtifact(
            "component", ["componentX"], [dependency]
        )
        compound = CompoundArtifact("compound", [component])
        self.artifacts = [dependency, compound]
        self.expect(
            'subgraph cluster_compound{',
            '  label="compound";',
            '  style="solid";',
            '  subgraph cluster_component{',
            '    label="component";',
            '    style="solid";',
            '    componentX[label="componentX"];',
            '  };',
            '};',
            'subgraph cluster_dependency{',
            '  label="dependency";',
            '  style="solid";',
            '  dependencyX[label="dependencyX"];',
            '};',
            'componentX->dependencyX',
            '  [lhead="cluster_dependency",ltail="cluster_component"];'
        )

    def testCompoundArtifactWithClient(self):
        component = AtomicArtifact("component", ["componentX"])
        compound = CompoundArtifact("compound", [component])
        client = AtomicArtifact("client", ["clientX"], [compound], [])
        self.artifacts = [client, compound]
        self.expect(
            'subgraph cluster_client{',
            '  label="client";',
            '  style="solid";',
            '  clientX[label="clientX"];',
            '};',
            'subgraph cluster_compound{',
            '  label="compound";',
            '  style="solid";',
            '  subgraph cluster_component{',
            '    label="component";',
            '    style="solid";',
            '    componentX[label="componentX"];',
            '  };',
            '};',
            'clientX->componentX',
            '  [lhead="cluster_compound",ltail="cluster_client"];'
        )

    def testCompoundArtifactWithClientOfComponent(self):
        component = AtomicArtifact("component", ["componentX"])
        compound = CompoundArtifact("compound", [component])
        client = AtomicArtifact("client", ["clientX"], [component], [])
        self.artifacts = [compound, client]
        self.expect(
            'subgraph cluster_client{',
            '  label="client";',
            '  style="solid";',
            '  clientX[label="clientX"];',
            '};',
            'subgraph cluster_compound{',
            '  label="compound";',
            '  style="solid";',
            '  subgraph cluster_component{',
            '    label="component";',
            '    style="solid";',
            '    componentX[label="componentX"];',
            '  };',
            '};',
            'clientX->componentX',
            '  [lhead="cluster_component",ltail="cluster_client"];'
        )

    def testSubAtomicArtifact(self):
        subatomic = SubatomicArtifact("subatomic", ["atomic1"])
        atomic = AtomicArtifact("atomic", ["atomic2"], [], [], [subatomic])
        self.artifacts = [atomic]
        self.expect(
            'subgraph cluster_atomic{',
            '  label="atomic";style="solid";',
            '  atomic2[label="atomic2"];',
            '  subgraph cluster_subatomic{',
            '    label="subatomic";style="dashed";',
            '    atomic1[label="atomic1"];',
            '  };',
            '};'
        )

    def testDependencyOnSubatomicArtifact(self):
        sub = SubatomicArtifact("sub", ["file2"])
        atomic = AtomicArtifact(
            "atomic",
            ["file1"],
            [],
            [],
            [sub]
        )
        client = AtomicArtifact("client", ["client"], [sub])
        self.artifacts = [atomic, client]
        self.expect(
            'client[label="client"];',
            'subgraph cluster_atomic{',
            '  label="atomic";',
            '  style="solid";',
            '  file1[label="file1"];',
            '  subgraph cluster_sub{',
            '    label="sub";',
            '    style="dashed";',
            '    file2[label="file2"];',
            '  };',
            '};',
            'client->file2[lhead="cluster_sub"];'
        )

    def testNamesWithForbidenCharacters(self):
        self.artifacts = [
            AtomicArtifact("foo/bar1.xxx", ["foo/bar1.xxx"]),
            AtomicArtifact("foo/bar2.xxx", ["foo/baz2.xxx"]),
            InputArtifact("foo/bar3.xxx"),
        ]
        self.expect(
            'foo_2fbar1_2exxx[label="foo/bar1.xxx"];',
            'foo_2fbar3_2exxx[label="foo/bar3.xxx"];',
            'subgraph cluster_foo_2fbar2_2exxx{',
            '  label="foo/bar2.xxx";',
            '  style="solid";',
            '  foo_2fbaz2_2exxx[label="foo/baz2.xxx"];',
            '};'
        )


class CheckTestCase(unittest.TestCase):
    def testCheckAtomicArtifact(self):
        AtomicArtifact("foo", ["foo"]).check()

    def testCheckInputArtifact(self):
        self.assertFalse(hasattr(InputArtifact("foo"), "check"))

    def testCheckSubatomicArtifact(self):
        self.assertFalse(hasattr(SubatomicArtifact("foo", ["foo"]), "check"))

    def testCheckCompoundArtifact(self):
        class Mock:
            def __init__(self):
                self.checked = False

            def check(self):
                self.checked = True

        mock = Mock()
        CompoundArtifact("foo", [mock]).check()
        self.assertTrue(mock.checked)


class MustBeProducedTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.fileExists = self.mocks.replace("_Artifact._fileExists")
        self.getFileModificationTime = self.mocks.replace("_Artifact._getFileModificationTime")

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.mocks.tearDown()

    def testAtomicArtifactMustBeProducedBecauseFileDoesNotExist(self):
        a = AtomicArtifact("foo", ["foo"])
        self.fileExists.expect("foo").andReturn(False)
        self.assertTrue(a._mustBeProduced([], []))

    def testAtomicArtifactMustBeProducedBecauseFileIsAssumedOld(self):
        a = AtomicArtifact("foo", ["foo"])
        self.assertTrue(a._mustBeProduced(["foo"], []))

    def testAtomicArtifactMustNotBeProducedBecauseFileIsAssumedNew(self):
        a = AtomicArtifact("foo", ["foo"])
        self.fileExists.expect("foo").andReturn(True)
        self.assertFalse(a._mustBeProduced([], ["foo"]))

    def testAtomicArtifactMustNotBeProduced(self):
        a = AtomicArtifact("foo", ["foo"])
        self.fileExists.expect("foo").andReturn(True)
        self.getFileModificationTime.expect("foo").andReturn(42)
        self.assertFalse(a._mustBeProduced([], []))

    def testAtomicArtifactMustBeProducedBecauseFileIsAssumedNewButDoesNotExist(self):
        a = AtomicArtifact("foo", ["foo"])
        self.fileExists.expect("foo").andReturn(False)
        self.assertTrue(a._mustBeProduced([], ["foo"]))

    def testAtomicArtifactMustBeProducedBecauseStrongDependencyIsNewer(self):
        a = AtomicArtifact("foo", ["foo"])
        b = AtomicArtifact("bar", ["bar"], [a])
        self.fileExists.expect("bar").andReturn(True)
        self.getFileModificationTime.expect("bar").andReturn(42)
        self.fileExists.expect("foo").andReturn(True)
        self.getFileModificationTime.expect("foo").andReturn(43)
        self.fileExists.expect("foo").andReturn(True)
        self.getFileModificationTime.expect("foo").andReturn(43)
        self.assertTrue(b._mustBeProduced([], []))

    def testAtomicArtifactMustBeProducedBecauseStrongDependencyMustBeProduced(self):
        a = AtomicArtifact("foo", ["foo"])
        b = AtomicArtifact("bar", ["bar"], [a])
        self.fileExists.expect("bar").andReturn(True)
        self.getFileModificationTime.expect("bar").andReturn(42)
        self.fileExists.expect("foo").andReturn(False)
        self.assertTrue(b._mustBeProduced([], []))

    def testAtomicArtifactMustNotBeProducedRegardlessOfOnlyDependency(self):
        a = AtomicArtifact("foo", ["foo"])
        b = AtomicArtifact("bar", ["bar"], [], [a])
        self.fileExists.expect("bar").andReturn(True)
        self.getFileModificationTime.expect("bar").andReturn(42)
        self.assertFalse(b._mustBeProduced([], []))

    def testCompoundArtifactMustBeProducedBecauseComponentMustBeProduced(self):
        a = AtomicArtifact("foo", ["foo"])
        b = CompoundArtifact("bar", [a])
        self.fileExists.expect("foo").andReturn(False)
        self.assertTrue(b._mustBeProduced([], []))

    def testCompoundArtifactMustNotBeProduced(self):
        a = AtomicArtifact("foo", ["foo"])
        b = CompoundArtifact("bar", [a])
        self.fileExists.expect("foo").andReturn(True)
        self.getFileModificationTime.expect("foo").andReturn(42)
        self.assertFalse(b._mustBeProduced([], []))

    def testInputArtifactMustNotBeProduced(self):
        a = InputArtifact("foo")
        self.assertFalse(a._mustBeProduced([], []))


class GetBuildActionTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.mocks.tearDown()

    def testAtomicArtifactWithoutDependenciesInCompoundArtifacts(self):
        atomic = AtomicArtifact("atomic", ["foo/bar/baz"])
        innerCompound = CompoundArtifact("innerCompound", [atomic])
        outerCompound = CompoundArtifact("outerCompound", [innerCompound])
        memo = _MemoForGetAction([], [], lambda a: a._createBaseTouchAction())

        m = self.mocks.replace("atomic._mustBeProduced")
        m.expect([], []).andReturn(True)
        m.expect([], []).andReturn(True)

        action = memo.getOrCreateActionForArtifact(outerCompound)
        self.assertEqual(action.getPreview(), ["mkdir foo/bar", "touch foo/bar/baz", "nop", "nop"])


if __name__ == "__main__":
    unittest.main()
