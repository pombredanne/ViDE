from __future__ import with_statement

import os.path
import unittest

import AnotherPyGraphvizAgain.Compounds as gvc
import AnotherPyGraphvizAgain.Raw as gvr
import ActionTree.Drawings
import ActionTree.StockActions as actions
import MockMockMock

import Misc.MockMockMock

from Artifact import Artifact, AtomicArtifact, CompoundArtifact, InputArtifact, BuildEmptyArtifact
from Action import Action

def assertActionHasGraph(test, a, g ):
    test.assertEqual(ActionTree.Drawings.ActionGraph(a).dotString(), g.dotString())

class EmptyArtifacts(unittest.TestCase):
    def testAtomic(self):
        AtomicArtifact("TestArtefact", [ "file" ], [], [], [], False)
        self.assertRaises( BuildEmptyArtifact, AtomicArtifact, "TestArtefact", [], [], [], [], False )

    def testCompound( self ):
        CompoundArtifact( "TestArtefact", [ AtomicArtifact( "TestArtefact", [ "file" ], [], [], [], False ) ], False )
        self.assertRaises( BuildEmptyArtifact, CompoundArtifact, "TestArtefact", [], False )

    def testInput( self ):
        InputArtifact( "TestArtefact", [ "file" ], False )
        self.assertRaises( BuildEmptyArtifact, InputArtifact, "TestArtefact", [], False )

class BasicAtomicArtifact(unittest.TestCase):
    def setUp( self ):
        unittest.TestCase.setUp( self )
        self.mocks = MockMockMock.Engine()
        self.artifact = AtomicArtifact("TestArtefact", ["tmp1/file1", "tmp2/file2"], [], [], [], False)
        self.productionAction = ActionTree.Action(None, "create file1 and file2")
        self.doGetProductionAction = self.mocks.create("self.doGetProductionAction")
        self.artifact.doGetProductionAction = self.doGetProductionAction.object

        self.fileIsMissing = self.mocks.create("self.fileIsMissing")
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.fileIsMissing.object

        self.fileIsMissing.expect("tmp1/file1").andReturn(False)
        self.fileIsMissing.expect("tmp2/file2").andReturn(True)
        self.doGetProductionAction.expect().andReturn(self.productionAction)

    def testGetProductionAction( self ):
        action = self.artifact.getProductionAction()

        model = gvr.Graph("action")
        n0 = gvr.Node("create_20file1_20and_20file2").set("label", "create file1 and file2")
        n1 = gvr.Node("mkdir_20tmp1").set("label", "mkdir tmp1")
        n2 = gvr.Node("mkdir_20tmp2").set("label", "mkdir tmp2")
        n3 = gvr.Node("rm_20tmp1_2ffile1").set("label", "rm tmp1/file1")
        n4 = gvr.Node("rm_20tmp2_2ffile2").set("label", "rm tmp2/file2")
        model.add(n0)
        model.add(n1)
        model.add(n2)
        model.add(n3)
        model.add(n4)
        model.add(gvr.Link(n0, n1))
        model.add(gvr.Link(n0, n2))
        model.add(gvr.Link(n0, n3))
        model.add(gvr.Link(n0, n4))

        assertActionHasGraph(self, action, model)

    def testGetProductionActionTwice( self ):
        action1 = self.artifact.getProductionAction()
        action2 = self.artifact.getProductionAction()
        self.assertTrue( action1 is action2 )

class BasicCompoundArtifact( Misc.MockMockMock.TestCase ):
    def setUp( self ):
        Misc.MockMockMock.TestCase.setUp( self )
        self.atomicArtifact1 = self.m.createMock( "self.atomicArtifact1", AtomicArtifact, "AtomicArtifact1", [ os.path.join( "tmp1", "file1" ) ], [], [], [], False )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.atomicArtifact2 = self.m.createMock( "self.atomicArtifact2", AtomicArtifact, "AtomicArtifact2", [ os.path.join( "tmp2", "file2" ) ], [], [], [], False )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.artifact = self.m.createMock( "self.artifact", CompoundArtifact, "CompoundArtifact", [ self.atomicArtifact1, self.atomicArtifact2 ], False )
        self.fileProductionAction1 = self.m.createMock( "self.fileProductionAction1", Action )
        self.fileProductionAction2 = self.m.createMock( "self.fileProductionAction2", Action )

    def recordGetProductionAction( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
        self.atomicArtifact1.doGetProductionAction().returns( self.fileProductionAction1 )
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp2", "file2" ) ).returns( True )
        self.atomicArtifact2.doGetProductionAction().returns( self.fileProductionAction2 )

#     def testGetProductionAction( self ):
#         self.recordGetProductionAction()
#         with self.m.unorderedGroup():
#             self.fileProductionAction1.computePreview().returns( "create file1" )
#             self.fileProductionAction2.computePreview().returns( "create file2" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()

#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "" )
#         n1 = Node( "create file1" )
#         n11 = Node( "mkdir -p tmp1" )
#         n12 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         n2 = Node( "create file2" )
#         n21 = Node( "mkdir -p tmp2" )
#         n22 = Node( "rm -f " + os.path.join( "tmp2", "file2" ) )
#         model.add( n0 )
#         model.add( n1 )
#         model.add( n11 )
#         model.add( n12 )
#         model.add( n2 )
#         model.add( n21 )
#         model.add( n22 )
#         model.add( Link( n0, n1 ) )
#         model.add( Link( n0, n2 ) )
#         model.add( Link( n1, n11 ) )
#         model.add( Link( n1, n12 ) )
#         model.add( Link( n2, n21 ) )
#         model.add( Link( n2, n22 ) )
        
#         assertActionHasGraph(self, action, model)

    # def testGetProductionActionTwice( self ):
    #     self.recordGetProductionAction()

    #     self.m.startTest()

    #     action1 = self.artifact.getProductionAction()
    #     action2 = self.artifact.getProductionAction()
    #     self.assertTrue( action1 is action2 )

# class ProductionReasons( Misc.MockMockMock.TestCase ):
#     def setUp( self ):
#         Misc.MockMockMock.TestCase.setUp( self )
#         self.strongDependency = self.m.createMock( "self.strongDependency", Artifact, "Dependency", False )
#         self.orderOnlyDependency = self.m.createMock( "self.orderOnlyDependency", Artifact, "Order only dependency", False )
#         self.automaticDependency = self.m.createMock( "self.automaticDependency", Artifact, "Automatic dependency", False )
#         self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "AtomicArtifact", [ os.path.join( "tmp1", "file1" ) ], [ self.strongDependency ], [ self.orderOnlyDependency ], [ self.automaticDependency ], False )
#         AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
#         self.productionAction = self.m.createMock( "self.productionAction", Action )
#         self.strongDependencyProductionAction = self.m.createMock( "self.strongDependencyProductionAction", Action )
#         self.orderOnlyDependencyProductionAction = self.m.createMock( "self.orderOnlyDependencyProductionAction", Action )
#         self.automaticDependencyProductionAction = self.m.createMock( "self.automaticDependencyProductionAction", Action )
#         self.strongDependency.getNewestFile = self.m.createMock( "self.strongDependency.getNewestFile" )
#         self.orderOnlyDependency.getNewestFile = self.m.createMock( "self.orderOnlyDependency.getNewestFile" )
#         self.automaticDependency.getNewestFile = self.m.createMock( "self.automaticDependency.getNewestFile" )
#         self.artifact.getOldestFile = self.m.createMock( "self.artifact.getOldestFile" )

#     def testGetProductionActionWithNoReasonToProduce( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.artifact.getOldestFile( [], [] ).returns( 1200001 )
#         self.strongDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.automaticDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         model.add( Node( "" ) )
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenFileIsMissing( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
#         self.artifact.doGetProductionAction().returns( self.productionAction )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )

#         self.productionAction.computePreview().returns( "create file1" )
        
#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "create file1" )
#         n3 = Node( "mkdir -p tmp1" )
#         n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         model.add( n0 )
#         model.add( n3 )
#         model.add( n4 )
#         model.add( Link( n0, n3 ) )
#         model.add( Link( n0, n4 ) )
        
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenOrderOnlyDependencyIsNewer( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.artifact.getOldestFile( [], [] ).returns( 1200001 )
#         self.strongDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.automaticDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.orderOnlyDependency.getNewestFile( [], [] ).returns( 1200002 ).isOptional() # Never called

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         model.add( Node( "" ) )
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenOrderOnlyDependencyMustBeProduced( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.artifact.getOldestFile( [], [] ).returns( 1200001 )
#         self.strongDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.automaticDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( True )
#         self.orderOnlyDependency.computeProductionAction( [], [], False, Misc.MockMockMock.DontCheck() ).returns( self.orderOnlyDependencyProductionAction )
        
#         self.orderOnlyDependencyProductionAction.computePreview().returns( "create orderOnlyDependency" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "" )
#         n1 = Node( "create orderOnlyDependency" )
#         model.add( n0 )
#         model.add( n1 )
#         model.add( Link( n0, n1 ) )
        
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenStrongDependencyIsNewer( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.artifact.getOldestFile( [], [] ).returns( 1200000 )
#         self.strongDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.artifact.doGetProductionAction().returns( self.productionAction )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )

#         self.productionAction.computePreview().returns( "create file1" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "create file1" )
#         n3 = Node( "mkdir -p tmp1" )
#         n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         model.add( n0 )
#         model.add( n3 )
#         model.add( n4 )
#         model.add( Link( n0, n3 ) )
#         model.add( Link( n0, n4 ) )
        
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenStrongDependencyMustBeProduced( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( True )
#         self.artifact.doGetProductionAction().returns( self.productionAction )
#         self.strongDependency.computeProductionAction( [], [], False, Misc.MockMockMock.DontCheck() ).returns( self.strongDependencyProductionAction )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )

#         self.productionAction.computePreview().returns( "create file1" )
#         self.strongDependencyProductionAction.computePreview().returns( "create strongDependency" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "create file1" )
#         n1 = Node( "create strongDependency" )
#         n3 = Node( "mkdir -p tmp1" )
#         n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         model.add( n0 )
#         model.add( n1 )
#         model.add( n3 )
#         model.add( n4 )
#         model.add( Link( n0, n1 ) )
#         model.add( Link( n0, n3 ) )
#         model.add( Link( n0, n4 ) )
        
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenAutomaticDependencyIsNewer( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.artifact.getOldestFile( [], [] ).returns( 1200001 )
#         self.strongDependency.getNewestFile( [], [] ).returns( 1200000 )
#         self.automaticDependency.getNewestFile( [], [] ).returns( 1200001 )
#         self.artifact.doGetProductionAction().returns( self.productionAction )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )

#         self.productionAction.computePreview().returns( "create file1" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "create file1" )
#         n3 = Node( "mkdir -p tmp1" )
#         n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         model.add( n0 )
#         model.add( n3 )
#         model.add( n4 )
#         model.add( Link( n0, n3 ) )
#         model.add( Link( n0, n4 ) )
        
#         assertActionHasGraph(self, action, model)

#     def testGetProductionActionWhenAutomaticDependencyMustBeProduced( self ):
#         AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
#         self.strongDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeIfMustBeProduced( [], [], False ).returns( True )
#         self.artifact.doGetProductionAction().returns( self.productionAction )
#         self.orderOnlyDependency.computeIfMustBeProduced( [], [], False ).returns( False )
#         self.automaticDependency.computeProductionAction( [], [], False, Misc.MockMockMock.DontCheck() ).returns( self.automaticDependencyProductionAction )

#         self.productionAction.computePreview().returns( "create file1" )
#         self.automaticDependencyProductionAction.computePreview().returns( "create automaticDependency" )

#         self.m.startTest()

#         action = self.artifact.getProductionAction()
        
#         model = Graph( "action" )
#         model.nodeAttr[ "shape" ] = "box"
#         n0 = Node( "create file1" )
#         n2 = Node( "create automaticDependency" )
#         n3 = Node( "mkdir -p tmp1" )
#         n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
#         model.add( n0 )
#         model.add( n2 )
#         model.add( n3 )
#         model.add( n4 )
#         model.add( Link( n0, n2 ) )
#         model.add( Link( n0, n3 ) )
#         model.add( Link( n0, n4 ) )
        
#         assertActionHasGraph(self, action, model)

class DrawGraph( Misc.MockMockMock.TestCase ):
    def __assertDotEqual(self, g1, g2):
        self.assertEqual(g1.dotString(), g2.dotString())

    def __cluster(self, name):
        return gvc.Cluster(name).set("label", name).set("style", "solid")

    def __node(self, id, label):
        return gvc.Node(id).set("label", label)

    def testAtomic( self ):
        artifact = AtomicArtifact("TestArtefact", ["tmp/file1", "tmp/file2"], [], [], [], False)

        cluster = self.__cluster("TestArtefact")
        cluster.add(self.__node("tmp_file1", "tmp/file1"))
        cluster.add(self.__node("tmp_file2", "tmp/file2"))

        self.__assertDotEqual(artifact.getGraphNode(), cluster)

    def testCompound( self ):
        atomic1 = AtomicArtifact("TestArtefact1", ["tmp/file1", "tmp/file2" ], [], [], [], False)
        atomic2 = AtomicArtifact("TestArtefact2", ["tmp/file3", "tmp/file4" ], [], [], [], False)
        artifact = CompoundArtifact("TestArtefact3", [atomic1, atomic2], False)

        mainCluster = self.__cluster("TestArtefact3")
        cluster = self.__cluster("TestArtefact1")
        cluster.add(self.__node("tmp_file1", "tmp/file1"))
        cluster.add(self.__node("tmp_file2", "tmp/file2"))
        mainCluster.add(cluster)
        cluster = self.__cluster("TestArtefact2")
        cluster.add(self.__node("tmp_file3", "tmp/file3"))
        cluster.add(self.__node("tmp_file4", "tmp/file4"))
        mainCluster.add(cluster)

        self.__assertDotEqual(artifact.getGraphNode(), mainCluster)

    def testStrongDependency( self ):
        artifact1 = AtomicArtifact("TestArtefact1", ["tmp/file1", "tmp/file2"], [], [], [], False)
        compound = CompoundArtifact("TestArtefact3", [artifact1], False)
        artifact2 = AtomicArtifact("TestArtefact2", ["tmp/file3", "tmp/file4"], [artifact1], [], [], False)

        g1 = gvc.Graph("project")
        cluster1 = self.__cluster("TestArtefact1")
        cluster1.add(self.__node("tmp_file1", "tmp/file1"))
        cluster1.add(self.__node("tmp_file2", "tmp/file2"))
        cluster = self.__cluster("TestArtefact3")
        cluster.add(cluster1)
        g1.add(cluster)
        cluster2 = self.__cluster("TestArtefact2")
        cluster2.add(self.__node("tmp_file3", "tmp/file3"))
        cluster2.add(self.__node("tmp_file4", "tmp/file4"))
        g1.add(cluster2)
        link = gvc.Link(cluster2, cluster1)
        g1.add(link)
        
        g2 = gvc.Graph("project")
        g2.add(artifact2.getGraphNode())
        g2.add(compound.getGraphNode())
        for l in artifact2.getGraphLinks():
            g2.add(l)
        for l in compound.getGraphLinks():
            g2.add(l)

        self.__assertDotEqual( g1, g2 )

    def testOrderOnlyDependency( self ):
        artifact1 = AtomicArtifact("TestArtefact1", ["tmp/file1", "tmp/file2"], [], [], [], False)
        compound = CompoundArtifact("TestArtefact3", [artifact1], False)
        artifact2 = AtomicArtifact("TestArtefact2", ["tmp/file3", "tmp/file4"], [], [artifact1], [], False)
        
        g1 = gvc.Graph("project")
        cluster1 = self.__cluster("TestArtefact1")
        cluster1.add(self.__node("tmp_file1", "tmp/file1"))
        cluster1.add(self.__node("tmp_file2", "tmp/file2"))
        cluster = self.__cluster("TestArtefact3")
        cluster.add(cluster1)
        g1.add(cluster)
        cluster2 = self.__cluster("TestArtefact2")
        cluster2.add(self.__node("tmp_file3", "tmp/file3"))
        cluster2.add(self.__node("tmp_file4", "tmp/file4"))
        g1.add(cluster2)
        link = gvc.Link(cluster2, cluster1)
        link.set("style", "dashed")
        g1.add(link)
        
        g2 = gvc.Graph("project")
        g2.add(artifact2.getGraphNode())
        g2.add(compound.getGraphNode())
        for l in artifact2.getGraphLinks():
            g2.add(l)
        for l in compound.getGraphLinks():
            g2.add(l)

        self.__assertDotEqual( g1, g2 )

unittest.main()
