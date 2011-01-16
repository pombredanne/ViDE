from __future__ import with_statement

import os.path
import unittest

from Misc.MockMockMock import TestCase
from Misc.Graphviz import Graph, Cluster, Node, Link

from Artifact import Artifact, AtomicArtifact, CompoundArtifact, InputArtifact, MonofileInputArtifact, CreateDirectoryAction
from Action import Action

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

    def testMonofileInput( self ):
        MonofileInputArtifact( "file" )
        self.assertRaises( Exception, MonofileInputArtifact, None )
        self.assertRaises( Exception, MonofileInputArtifact, "" )

class BasicAtomicArtifact( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "TestArtefact", [ os.path.join( "tmp1", "file1" ), os.path.join( "tmp2", "file2" ) ], [], [], [] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )

    def recordGetProductionAction( self ):
        for i in range( 2 ):
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

        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
                AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )
                self.atomicArtifact1.doGetProductionAction().returns( self.fileProductionAction1 )
            with self.m.orderedGroup():
                AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp2", "file2" ) ).returns( True )
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
        self.dependency = self.m.createMock( "self.dependency", Artifact, "Dependency" )
        self.orderOnlyDependency = self.m.createMock( "self.orderOnlyDependency", Artifact, "Order only dependency" )
        self.automaticDependency = self.m.createMock( "self.automaticDependency", Artifact, "Automatic dependency" )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "AtomicArtifact", [ os.path.join( "tmp1", "file1" ) ], [ self.dependency ], [ self.orderOnlyDependency ], [ self.automaticDependency ] )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )
        self.dependencyProductionAction = self.m.createMock( "self.dependencyProductionAction", Action )
        self.orderOnlyDependencyProductionAction = self.m.createMock( "self.orderOnlyDependencyProductionAction", Action )
        self.dependency.getNewestFile = self.m.createMock( "self.dependency.getNewestFile" )
        self.orderOnlyDependency.getNewestFile = self.m.createMock( "self.orderOnlyDependency.getNewestFile" )
        self.automaticDependency.getNewestFile = self.m.createMock( "self.automaticDependency.getNewestFile" )
        self.artifact.getOldestFile = self.m.createMock( "self.artifact.getOldestFile" )

    def testGetProductionActionWithNoReasonToProduce( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.dependency.mustBeProduced().returns( False )
        self.automaticDependency.mustBeProduced().returns( False )
        self.artifact.getOldestFile().returns( 1200001 )
        self.dependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.mustBeProduced().returns( False )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        model.add( Node( "" ) )
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyIsNewer( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
        self.dependency.mustBeProduced().returns( False )
        self.automaticDependency.mustBeProduced().returns( False )
        self.artifact.getOldestFile().returns( 1200001 )
        self.dependency.getNewestFile().returns( 1200000 )
        self.automaticDependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.mustBeProduced().returns( False )
        self.orderOnlyDependency.getNewestFile().returns( 1200002 ).isOptional() # Never called

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        model.add( Node( "" ) )
        self.assertTrue( actionHasGraph( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyMustBeProduced( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.automaticDependency.mustBeProduced().returns( False )
            self.artifact.getOldestFile().returns( 1200001 )
            self.dependency.getNewestFile().returns( 1200000 )
            self.automaticDependency.getNewestFile().returns( 1200000 )
            if i == 0:
                self.orderOnlyDependency.mustBeProduced().returns( True )

        self.dependency.mustBeProduced().returns( False )
        self.orderOnlyDependency.mustBeProduced().returns( True )
        self.orderOnlyDependency.computeProductionAction().returns( self.orderOnlyDependencyProductionAction )
        self.automaticDependency.mustBeProduced().returns( False )
        self.orderOnlyDependencyProductionAction.computePreview().returns( "create orderOnlyDependency" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "" )
        n1 = Node( "" )
        n2 = Node( "create orderOnlyDependency" )
        n3 = Node( "" )
        model.add( n0 )
        model.add( n1 )
        model.add( n2 )
        model.add( n3 )
        model.add( Link( n0, n1 ) )
        model.add( Link( n0, n2 ) )
        model.add( Link( n0, n3 ) )
        
        # This test often fails, because several nodes have the same preview,
        # Which is not handled well by Graphviz.grah.areSame
        self.assertTrue( actionHasGraph( action, model ) )

    def getProductionActionAndPreview( self ):
        self.recordGetProductionActionPreview()

        self.m.startTest()

        action = self.artifact.getProductionAction()
        
        model = Graph( "action" )
        model.nodeAttr[ "shape" ] = "box"
        n0 = Node( "create file1" )
        n1 = Node( "create dependency" )
        n2 = Node( "create orderOnlyDependency" )
        n3 = Node( "mkdir -p tmp1" )
        n4 = Node( "rm -f " + os.path.join( "tmp1", "file1" ) )
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

    def recordGetProductionActionPreview( self ):
        CreateDirectoryAction._CreateDirectoryAction__all = dict()
    
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.dependency.mustBeProduced().returns( True )
        self.dependency.computeProductionAction().returns( self.dependencyProductionAction )
        self.orderOnlyDependency.mustBeProduced().returns( True )
        self.orderOnlyDependency.computeProductionAction().returns( self.orderOnlyDependencyProductionAction )
        self.automaticDependency.mustBeProduced().returns( True )
        self.automaticDependency.computeProductionAction().returns( self.dependencyProductionAction )

        self.productionAction.computePreview().returns( "create file1" )
        with self.m.unorderedGroup():
            self.dependencyProductionAction.computePreview().returns( "create dependency" )
            self.orderOnlyDependencyProductionAction.computePreview().returns( "create orderOnlyDependency" )

    def testGetProductionActionWhenFileIsMissing( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( True )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenDependencyMustBeProduced( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
            self.dependency.mustBeProduced().returns( True )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenDependencyIsNewer( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.automaticDependency.mustBeProduced().returns( False )
            self.artifact.getOldestFile().returns( 1200000 )
            self.dependency.getNewestFile().returns( 1200000 )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenAutomaticDependencyMustBeProduced( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.automaticDependency.mustBeProduced().returns( True )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenAutomaticDependencyIsNewer( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( os.path.join( "tmp1", "file1" ) ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.automaticDependency.mustBeProduced().returns( False )
            self.artifact.getOldestFile().returns( 1200001 )
            self.dependency.getNewestFile().returns( 1200000 )
            self.automaticDependency.getNewestFile().returns( 1200001 )

        self.getProductionActionAndPreview()

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
