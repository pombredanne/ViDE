from __future__ import with_statement

import os.path
import unittest

from Misc.MockMockMock import TestCase
from Misc.Graphviz import Graph, Cluster, Node, Link

from Artifact import Artifact, AtomicArtifact, CompoundArtifact, InputArtifact, MonofileInputArtifact, CreateDirectoryAction
from Action import Action, NullAction

def actionHasGraph( a, g ):
    return Graph.areSame( a.getGraph(), g )

class EmptyArtifacts( TestCase ):
    def testAtomic( self ):
        AtomicArtifact( "TestArtefact", [ "file" ], [], [], [] )
        self.assertRaises( Exception, AtomicArtifact, "TestArtefact", [], [], [], [] )

    def testCompound( self ):
        CompoundArtifact( "TestArtefact", [ AtomicArtifact( "TestArtefact", [ "file" ], [], [], [] ) ] )
        self.assertRaises( Exception, CompoundArtifact, "TestArtefact", [] )

    def testInput( self ):
        InputArtifact( "TestArtefact", [ "file" ] )
        self.assertRaises( Exception, InputArtifact, "TestArtefact", [] )

class BasicAtomicArtifact( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "TestArtefact", [ os.path.join( "tmp1", "file1" ), os.path.join( "tmp2", "file2" ) ], [], [], [] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )

    def recordGetProductionAction( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp2", "file2" ) ).returns( True )
        self.artifact.doGetProductionAction().returns( self.productionAction )

    def testGetProductionAction( self ):
        self.recordGetProductionAction()
        self.productionAction.computePreview().returns( "create file1 and file2" )

        self.m.startTest()

        action = self.artifact.getProductionAction()

        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1 and file2" )
        n1 = Node( "mkdir -p tmp1" )
        n2 = Node( "mkdir -p tmp2" )
        n3 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        n4 = Node( "rm -f " + os.path.join( "tmp2", "file2" ) )
        model.add( n0 )
        model.add( n1 )
        model.add( n2 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n1 ) )
        model.add( Link( n0, n2 ) )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionTwice( self ):
        self.recordGetProductionAction()

        self.m.startTest()

        action1 = self.artifact.getProductionAction()
        action2 = self.artifact.getProductionAction()
        self.assertTrue( action1 is action2 )

class BasicCompoundArtifact( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.atomicArtifact1 = self.m.createMock( "self.atomicArtifact1", AtomicArtifact, "AtomicArtifact1", [ os.path.join( "tmp1", "file1" ) ], [], [], [] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.atomicArtifact2 = self.m.createMock( "self.atomicArtifact2", AtomicArtifact, "AtomicArtifact2", [ os.path.join( "tmp2", "file2" ) ], [], [], [] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.artifact = self.m.createMock( "self.artifact", CompoundArtifact, "CompoundArtifact", [ self.atomicArtifact1, self.atomicArtifact2 ] )
        self.fileProductionAction1 = self.m.createMock( "self.fileProductionAction1", Action )
        self.fileProductionAction2 = self.m.createMock( "self.fileProductionAction2", Action )

    def recordGetProductionAction( self ):
        CreateDirectoryAction._CreateDirectoryAction__all = dict()

        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
        self.atomicArtifact1.doGetProductionAction().returns( self.fileProductionAction1 )
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp2", "file2" ) ).returns( True )
        self.atomicArtifact2.doGetProductionAction().returns( self.fileProductionAction2 )

    def testGetProductionAction( self ):
        self.recordGetProductionAction()
        with self.m.unorderedGroup():
            self.fileProductionAction1.computePreview().returns( "create file1" )
            self.fileProductionAction2.computePreview().returns( "create file2" )

        self.m.startTest()

        action = self.artifact.getProductionAction()

        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "" )
        n1 = Node( "create file1" )
        n11 = Node( "mkdir -p tmp1" )
        n12 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        n2 = Node( "create file2" )
        n21 = Node( "mkdir -p tmp2" )
        n22 = Node( "rm -f " + os.path.join( "tmp2", "file2" ) )
        model.add( n0 )
        model.add( n1 )
        model.add( n11 )
        model.add( n12 )
        model.add( n2 )
        model.add( n21 )
        model.add( n22 )
        model.add( Link( n0, n1 ) )
        model.add( Link( n0, n2 ) )
        model.add( Link( n1, n11 ) )
        model.add( Link( n1, n12 ) )
        model.add( Link( n2, n21 ) )
        model.add( Link( n2, n22 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionTwice( self ):
        self.recordGetProductionAction()

        self.m.startTest()

        action1 = self.artifact.getProductionAction()
        action2 = self.artifact.getProductionAction()
        self.assertTrue( action1 is action2 )

class ProductionReasons( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.strongDependency = self.m.createMock( "self.strongDependency", Artifact, "Dependency" )
        self.orderOnlyDependency = self.m.createMock( "self.orderOnlyDependency", Artifact, "Order only dependency" )
        self.automaticDependency = self.m.createMock( "self.automaticDependency", Artifact, "Automatic dependency" )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "AtomicArtifact", [ os.path.join( "tmp1", "file1" ) ], [ self.strongDependency ], [ self.orderOnlyDependency ], [ self.automaticDependency ] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )
        self.strongDependencyProductionAction = self.m.createMock( "self.strongDependencyProductionAction", Action )
        self.orderOnlyDependencyProductionAction = self.m.createMock( "self.orderOnlyDependencyProductionAction", Action )
        self.automaticDependencyProductionAction = self.m.createMock( "self.automaticDependencyProductionAction", Action )
        self.strongDependency.getNewestFile = self.m.createMock( "self.strongDependency.getNewestFile" )
        self.orderOnlyDependency.getNewestFile = self.m.createMock( "self.orderOnlyDependency.getNewestFile" )
        self.automaticDependency.getNewestFile = self.m.createMock( "self.automaticDependency.getNewestFile" )
        self.artifact.getOldestFile = self.m.createMock( "self.artifact.getOldestFile" )

    def testGetProductionActionWithNoReasonToProduce( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )
        self.artifact.getOldestFile().returns( 1200001 )
        self.strongDependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenFileIsMissing( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )

        self.productionAction.computePreview().returns( "create file1" )
        
        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        model.add( n0 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyIsNewer( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )
        self.artifact.getOldestFile().returns( 1200001 )
        self.strongDependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )
        self.orderOnlyDependency.getNewestFile().returns( 1200002 ).isOptional() # Never called

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyMustBeProduced( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )
        self.artifact.getOldestFile().returns( 1200001 )
        self.strongDependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.computeProductionAction().returns( self.orderOnlyDependencyProductionAction )
        
        self.orderOnlyDependencyProductionAction.computePreview().returns( "create orderOnlyDependency" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "" )
        n1 = Node( "create orderOnlyDependency" )
        model.add( n0 )
        model.add( n1 )
        model.add( Link( n0, n1 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenStrongDependencyIsNewer( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )
        self.artifact.getOldestFile().returns( 1200000 )
        self.strongDependency.getNewestFile().returns( 1200000 )
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )

        self.productionAction.computePreview().returns( "create file1" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        model.add( n0 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenStrongDependencyMustBeProduced( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( self.strongDependencyProductionAction )
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )

        self.productionAction.computePreview().returns( "create file1" )
        self.strongDependencyProductionAction.computePreview().returns( "create strongDependency" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n1 = Node( "create strongDependency" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        model.add( n0 )
        model.add( n1 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n1 ) )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenAutomaticDependencyIsNewer( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( NullAction() )
        self.artifact.getOldestFile().returns( 1200001 )
        self.strongDependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200001 )
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )

        self.productionAction.computePreview().returns( "create file1" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        model.add( n0 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenAutomaticDependencyMustBeProduced( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.strongDependency.computeProductionAction().returns( NullAction() )
        self.automaticDependency.computeProductionAction().returns( self.automaticDependencyProductionAction )
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.orderOnlyDependency.computeProductionAction().returns( NullAction() )

        self.productionAction.computePreview().returns( "create file1" )
        self.automaticDependencyProductionAction.computePreview().returns( "create automaticDependency" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n2 = Node( "create automaticDependency" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
        model.add( n0 )
        model.add( n2 )
        model.add( n3 )
        model.add( n4 )
        model.add( Link( n0, n2 ) )
        model.add( Link( n0, n3 ) )
        model.add( Link( n0, n4 ) )
        
        self.assertTrue( actionHasGraph( action, model ) )

class DrawGraph( TestCase ):
    def testAtomic( self ):
        artifact = AtomicArtifact( "TestArtefact", [ os.path.join( "tmp", "file1" ), os.path.join( "tmp", "file2" ) ], [], [], [] )
        
        g1 = Graph( "project" )
        cluster = Cluster( "TestArtefact" )
        cluster.add( Node( os.path.join( "tmp", "file1" ) ) )
        cluster.add( Node( os.path.join( "tmp", "file2" ) ) )
        g1.add( cluster )
        
        g2 = Graph( "project" )
        g2.add( artifact.getGraphNode() )
        
        self.assertTrue( Graph.areSame( g1, g2 ) )

    def testCompound( self ):
        atomic1 = AtomicArtifact( "TestArtefact1", [ os.path.join( "tmp", "file1" ), os.path.join( "tmp", "file2" ) ], [], [], [] )
        atomic2 = AtomicArtifact( "TestArtefact2", [ os.path.join( "tmp", "file3" ), os.path.join( "tmp", "file4" ) ], [], [], [] )
        artifact = CompoundArtifact( "TestArtefact3", [ atomic1, atomic2 ] )
        
        g1 = Graph( "project" )
        mainCluster = Cluster( "TestArtefact3" )
        cluster = Cluster( "TestArtefact1" )
        cluster.add( Node( os.path.join( "tmp", "file1" ) ) )
        cluster.add( Node( os.path.join( "tmp", "file2" ) ) )
        mainCluster.add( cluster )
        cluster = Cluster( "TestArtefact2" )
        cluster.add( Node( os.path.join( "tmp", "file3" ) ) )
        cluster.add( Node( os.path.join( "tmp", "file4" ) ) )
        mainCluster.add( cluster )
        g1.add( mainCluster )
        
        g2 = Graph( "project" )
        g2.add( artifact.getGraphNode() )
        
        self.assertTrue( Graph.areSame( g1, g2 ) )

    def testStrongDependency( self ):
        artifact1 = AtomicArtifact( "TestArtefact1", [ os.path.join( "tmp", "file1" ), os.path.join( "tmp", "file2" ) ], [], [], [] )
        compound = CompoundArtifact( "TestArtefact3", [ artifact1 ] )
        artifact2 = AtomicArtifact( "TestArtefact2", [ os.path.join( "tmp", "file3" ), os.path.join( "tmp", "file4" ) ], [ artifact1 ], [], [] )
        
        g1 = Graph( "project" )
        cluster1 = Cluster( "TestArtefact1" )
        cluster1.add( Node( os.path.join( "tmp", "file1" ) ) )
        cluster1.add( Node( os.path.join( "tmp", "file2" ) ) )
        cluster = Cluster( "TestArtefact3" )
        cluster.add( cluster1 )
        g1.add( cluster )
        cluster2 = Cluster( "TestArtefact2" )
        cluster2.add( Node( os.path.join( "tmp", "file3" ) ) )
        cluster2.add( Node( os.path.join( "tmp", "file4" ) ) )
        g1.add( cluster2 )
        link = Link( cluster2, cluster1 )
        g1.add( link )
        
        g2 = Graph( "project" )
        g2.add( artifact2.getGraphNode() )
        g2.add( compound.getGraphNode() )
        for l in artifact2.getGraphLinks():
            g2.add( l )
        for l in compound.getGraphLinks():
            g2.add( l )

        self.assertTrue( Graph.areSame( g1, g2 ) )

    def testOrderOnlyDependency( self ):
        artifact1 = AtomicArtifact( "TestArtefact1", [ os.path.join( "tmp", "file1" ), os.path.join( "tmp", "file2" ) ], [], [], [] )
        compound = CompoundArtifact( "TestArtefact3", [ artifact1 ] )
        artifact2 = AtomicArtifact( "TestArtefact2", [ os.path.join( "tmp", "file3" ), os.path.join( "tmp", "file4" ) ], [], [ artifact1 ], [] )
        
        g1 = Graph( "project" )
        cluster1 = Cluster( "TestArtefact1" )
        cluster1.add( Node( os.path.join( "tmp", "file1" ) ) )
        cluster1.add( Node( os.path.join( "tmp", "file2" ) ) )
        cluster = Cluster( "TestArtefact3" )
        cluster.add( cluster1 )
        g1.add( cluster )
        cluster2 = Cluster( "TestArtefact2" )
        cluster2.add( Node( os.path.join( "tmp", "file3" ) ) )
        cluster2.add( Node( os.path.join( "tmp", "file4" ) ) )
        g1.add( cluster2 )
        link = Link( cluster2, cluster1 )
        link.attr[ "style" ] = "dashed"
        g1.add( link )
        
        g2 = Graph( "project" )
        g2.add( artifact2.getGraphNode() )
        g2.add( compound.getGraphNode() )
        for l in artifact2.getGraphLinks():
            g2.add( l )
        for l in compound.getGraphLinks():
            g2.add( l )

        self.assertTrue( Graph.areSame( g1, g2 ) )

unittest.main()
