import unittest
import traceback
import os.path

import AnotherPyGraphvizAgain.Compounds as gv


class _Artifact(object):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class _ArtifactWithFiles(_Artifact):
    def __init__(self, name, files):
        _Artifact.__init__(self, name)
        assert len(files) > 0
        self.__files = set(files)

    @property
    def files(self):
        return sorted(self.__files)

    def _createGraphNodeAndLinks(self, memo):
        if len(self.__files) == 1 and self.files[0] == self.name:
            node = gv.Node(self.name)
        else:
            node = gv.Cluster(self.name)
            node.set("label", self.name)
            node.set("style", "solid")
            for f in self.files:
                node.add(gv.Node(f))
        return node, []


class InputArtifact(_ArtifactWithFiles):
    """
    An artifact that never needs to be produced
    """


class AtomicArtifact(_ArtifactWithFiles):
    """
    An artifact that is produced by a single action.
    """

    def __init__(self, name, files,
                 strongDependencies, orderOnlyDependencies,
                 subatomicArtifacts=[]):
        """
        :param: strongDependencies If a strong dependency is rebuilt,
        then the artifact must be rebuilt.

        :param: orderOnlyDependencies If an order-only dependency is absent,
        then it must be build before the artifact. But if an order-only
        dependency is rebuilt, the artifact doesn't need to be rebuilt.
        """
        _ArtifactWithFiles.__init__(self, name, files)
        self.__strongDependencies = strongDependencies
        self.__orderOnlyDependencies = orderOnlyDependencies
        self.__subs = subatomicArtifacts

    def _getRelatedNodes(self):
        return self.__strongDependencies + self.__orderOnlyDependencies

    def _createGraphNodeAndLinks(self, memo):
        if (
            len(self.__subs) == 0
            and len(self.files) == 1
            and self.files[0] == self.name
        ):
            node = gv.Node(self.name)
        else:
            node = gv.Cluster(self.name)
            node.set("label", self.name)
            node.set("style", "solid")
            for sub in self.__subs:
                subNode = memo.getOrCreateNode(sub)
                subNode.set("style", "dashed")
                node.add(subNode)
            for f in self.files:
                node.add(gv.Node(f))

        links = []
        for d in self.__strongDependencies:
            links.append(gv.Link(node, memo.getOrCreateNode(d)))
        for d in self.__orderOnlyDependencies:
            link = gv.Link(node, memo.getOrCreateNode(d))
            link.set("style", "dashed")
            links.append(link)

        return node, links


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
        node = gv.Cluster(self.name)
        node.set("label", self.name)
        node.set("style", "solid")
        for component in self.__components:
            node.add(memo.getOrCreateNode(component))
        return node, []


class SubatomicArtifact(_ArtifactWithFiles):
    """
    An artifact that is produced by the production action of its
    atomicArtifact, but is useful on its own, for example as a dependency.
    """


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

    graph = gv.Graph("artifact")
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
            'digraph "artifact" ' +
            '{compound="true";ranksep="1";node [shape="box"];'
        )
        expectedEndOfDotString = '}'

        for (_, _, functionName, _) in traceback.extract_stack():
            if functionName.startswith("test"):
                testName = self.__class__.__name__ + "." + functionName
                break

        graph = getGraphOfArtifacts(self.artifacts)
        fileName = os.path.join(os.path.dirname(__file__), testName + ".png")
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
            "".join(expectedMidleOfDotString)
        )
        self.assertEqual(
            dotString[-len(expectedEndOfDotString):],
            expectedEndOfDotString
        )

    def testSingleFileInputArtifact(self):
        self.artifacts = [InputArtifact("input", ["input"])]
        self.expect(
            'input;'
        )

    def testMultiFilesInputArtifact(self):
        self.artifacts = [InputArtifact("input", ["input1", "input2"])]
        self.expect(
            'subgraph cluster_input{',
            'label="input";style="solid";input1;input2;};'
        )

    def testSingleFileAtomicArtifact(self):
        self.artifacts = [AtomicArtifact("atomic", ["atomic"], [], [])]
        self.expect(
            'atomic;'
        )

    def testMultiFilesAtomicArtifact(self):
        self.artifacts = [
            AtomicArtifact("atomic", ["atomic1", "atomic2"], [], [])
        ]
        self.expect(
            'subgraph cluster_atomic{'
            'label="atomic";style="solid";atomic1;atomic2;};'
        )

    def testAtomicArtifactWithDependencies_SingleFile(self):
        strong = InputArtifact("strong", ["strong"])
        order = InputArtifact("order", ["order"])
        atomic = AtomicArtifact("atomic", ["atomic"], [strong], [order])
        self.artifacts = [atomic, strong, order]
        self.expect(
            'atomic;order;strong;',
            'atomic->order[style="dashed"];atomic->strong;'
        )

    def testAtomicArtifactWithDependencies_MultiFiles(self):
        strong = InputArtifact("strong", ["strong_"])
        order = InputArtifact("order", ["order_"])
        atomic = AtomicArtifact("atomic", ["atomic_"], [strong], [order])
        self.artifacts = [atomic, strong, order]
        self.expect(
            'subgraph cluster_atomic{label="atomic";style="solid";atomic_;};',
            'subgraph cluster_order{label="order";style="solid";order_;};',
            'subgraph cluster_strong{label="strong";style="solid";strong_;};',
            'atomic_->order_[',
            'lhead="cluster_order",ltail="cluster_atomic",style="dashed"',
            '];',
            'atomic_->strong_[lhead="cluster_strong",ltail="cluster_atomic"];'
        )

    def testCompoundArtifactWithoutDependencies(self):
        component1 = InputArtifact("component1", ["component1"])
        component2 = AtomicArtifact("component2", ["component2"], [], [])
        compound = CompoundArtifact("compound", [component1, component2])
        self.artifacts = [compound]
        self.expect(
            'subgraph cluster_compound{'
            'label="compound";style="solid";component1;component2;};'
        )

    def testCompoundArtifactWithDependencies(self):
        dependency = InputArtifact("dependency", ["dependency_"])
        component = AtomicArtifact(
            "component", ["component_"], [dependency], []
        )
        compound = CompoundArtifact("compound", [component])
        self.artifacts = [dependency, compound]
        self.expect(
            'subgraph cluster_compound{label="compound";style="solid";',
            'subgraph cluster_component{label="component";style="solid";',
            'component_;};};',
            'subgraph cluster_dependency{label="dependency";style="solid";',
            'dependency_;};',
            'component_->dependency_',
            '[lhead="cluster_dependency",ltail="cluster_component"];'
        )

    def testCompoundArtifactWithClient(self):
        component = AtomicArtifact("component", ["component_"], [], [])
        compound = CompoundArtifact("compound", [component])
        client = AtomicArtifact("client", ["client_"], [compound], [])
        self.artifacts = [client, compound]
        self.expect(
            'subgraph cluster_client{label="client";style="solid";client_;};',
            'subgraph cluster_compound{label="compound";style="solid";',
            'subgraph cluster_component{label="component";style="solid";',
            'component_;};};',
            'client_->component_',
            '[lhead="cluster_compound",ltail="cluster_client"];'
        )

    def testCompoundArtifactWithClientOfComponent(self):
        component = AtomicArtifact("component", ["component_"], [], [])
        compound = CompoundArtifact("compound", [component])
        client = AtomicArtifact("client", ["client_"], [component], [])
        self.artifacts = [compound, client]
        self.expect(
            'subgraph cluster_client{label="client";style="solid";client_;};',
            'subgraph cluster_compound{label="compound";style="solid";',
            'subgraph cluster_component{label="component";style="solid";',
            'component_;};};',
            'client_->component_',
            '[lhead="cluster_component",ltail="cluster_client"];'
        )

    def testSubAtomicArtifact(self):
        subatomic = SubatomicArtifact("subatomic", ["atomic1"])
        atomic = AtomicArtifact("atomic", ["atomic2"], [], [], [subatomic])
        self.artifacts = [atomic]
        self.expect(
            'subgraph cluster_atomic{label="atomic";style="solid";',
            'atomic2;',
            'subgraph cluster_subatomic',
            '{label="subatomic";style="dashed";atomic1;};};'
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
        client = AtomicArtifact("client", ["client"], [sub], [], [])
        self.artifacts = [atomic, client]
        self.expect(
            'client;',
            'subgraph cluster_atomic{label="atomic";style="solid";',
            'file1;subgraph cluster_sub{label="sub";style="dashed";file2;};};',
            'client->file2[lhead="cluster_sub"];'
        )


if __name__ == "__main__":
    unittest.main()
