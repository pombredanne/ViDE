#!/usr/bin/env python

from __future__ import with_statement

import unittest

from Misc.MockMockMock import TestCase

from Artifact import AtomicArtifact, CompoundArtifact, ProduceableArtifact
from Action import Action, ActionModel

class EmptyArtifacts( TestCase ):
    def testAtomic( self ):
        AtomicArtifact( "TestArtefact", [ "file" ], [], [], True )
        self.assertRaises( Exception, AtomicArtifact, "TestArtefact", [], [], [], True )
    def testCompound( self ):
        CompoundArtifact( "TestArtefact", [ AtomicArtifact( "TestArtefact", [ "file" ], [], [], True ) ], True )
        self.assertRaises( Exception, CompoundArtifact, "TestArtefact", [], True )

class BasicAtomicArtifact( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "TestArtefact", [ "/tmp1/file1", "/tmp2/file2" ], [], [], True )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )

    def recordGetProductionAction( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp2/file2" ).returns( True )
        self.artifact.doGetProductionAction().returns( self.productionAction )

    def testGetProductionAction( self ):
        self.recordGetProductionAction()
        self.productionAction.doPreview().returns( "create file1 and file2" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( {
            "create file1 and file2": {
                "mkdir -p /tmp1": {},
                "mkdir -p /tmp2": {},
                "rm -f /tmp1/file1": {},
                "rm -f /tmp2/file2": {}
            }
        } )
        self.assertTrue( Action.areSame( action, model ) )

    def testGetProductionActionTwice( self ):
        self.recordGetProductionAction()

        self.m.startTest()

        action1 = self.artifact.getProductionAction()
        action2 = self.artifact.getProductionAction()
        self.assertTrue( action1 is action2 )

class BasicCompoundArtifact( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.atomicArtifact1 = self.m.createMock( "self.atomicArtifact1", AtomicArtifact, "AtomicArtifact1", [ "/tmp1/file1" ], [], [], True )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.atomicArtifact2 = self.m.createMock( "self.atomicArtifact2", AtomicArtifact, "AtomicArtifact2", [ "/tmp2/file2" ], [], [], True )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.artifact = self.m.createMock( "self.artifact", CompoundArtifact, "CompoundArtifact", [ self.atomicArtifact1, self.atomicArtifact2 ], True )
        self.fileProductionAction1 = self.m.createMock( "self.fileProductionAction1", Action )
        self.fileProductionAction2 = self.m.createMock( "self.fileProductionAction2", Action )

    def recordGetProductionAction( self ):
        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( True )
                AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( True )
                self.atomicArtifact1.doGetProductionAction().returns( self.fileProductionAction1 )
            with self.m.orderedGroup():
                AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp2/file2" ).returns( True )
                AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp2/file2" ).returns( True )
                self.atomicArtifact2.doGetProductionAction().returns( self.fileProductionAction2 )

    def testGetProductionAction( self ):
        self.recordGetProductionAction()
        with self.m.unorderedGroup():
            self.fileProductionAction1.doPreview().returns( "create file1" )
            self.fileProductionAction2.doPreview().returns( "create file2" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( {
            "": {
                "create file1": {
                    "mkdir -p /tmp1": {},
                    "rm -f /tmp1/file1": {},
                },
                "create file2": {
                    "mkdir -p /tmp2": {},
                    "rm -f /tmp2/file2": {}
                }
            }
        } )
        self.assertTrue( Action.areSame( action, model ) )

    def testGetProductionActionTwice( self ):
        self.recordGetProductionAction()

        self.m.startTest()

        action1 = self.artifact.getProductionAction()
        action2 = self.artifact.getProductionAction()
        self.assertTrue( action1 is action2 )

class ProductionReasons( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.dependency = self.m.createMock( "self.dependency", ProduceableArtifact, "Dependency", True )
        self.orderOnlyDependency = self.m.createMock( "self.orderOnlyDependency", ProduceableArtifact, "Order only dependency", True )
        self.artifact = self.m.createMock( "self.artifact", AtomicArtifact, "AtomicArtifact", [ "/tmp1/file1" ], [ self.dependency ], [ self.orderOnlyDependency ], True )
        AtomicArtifact._AtomicArtifact__fileIsMissing = self.m.createMock( "AtomicArtifact._AtomicArtifact__fileIsMissing" )
        self.productionAction = self.m.createMock( "self.productionAction", Action )
        self.dependencyProductionAction = self.m.createMock( "self.dependencyProductionAction", Action )
        self.orderOnlyDependencyProductionAction = self.m.createMock( "self.orderOnlyDependencyProductionAction", Action )
        self.dependency.getNewestFile = self.m.createMock( "self.dependency.getNewestFile" )
        self.orderOnlyDependency.getNewestFile = self.m.createMock( "self.orderOnlyDependency.getNewestFile" )
        self.artifact.getOldestFile = self.m.createMock( "self.artifact.getOldestFile" )

    def testGetProductionActionWithNoReasonToProduce( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
        self.dependency.mustBeProduced().returns( False )
        self.artifact.getOldestFile().returns( 1200001 )
        self.dependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.mustBeProduced().returns( False )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( { "": {} } )
        self.assertTrue( Action.areSame( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyIsNewer( self ):
        AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
        self.dependency.mustBeProduced().returns( False )
        self.artifact.getOldestFile().returns( 1200001 )
        self.dependency.getNewestFile().returns( 1200000 )
        self.orderOnlyDependency.mustBeProduced().returns( False )
        self.orderOnlyDependency.getNewestFile().returns( 1200002 ).isOptional() # Never called

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( { "": {} } )
        self.assertTrue( Action.areSame( action, model ) )

    def testGetProductionActionWhenOrderOnlyDependencyMustBeProduced( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.artifact.getOldestFile().returns( 1200001 )
            self.dependency.getNewestFile().returns( 1200000 )
            if i == 0:
                self.orderOnlyDependency.mustBeProduced().returns( True )

        self.dependency.mustBeProduced().returns( False )
        self.orderOnlyDependency.mustBeProduced().returns( True )
        self.orderOnlyDependency.computeProductionAction().returns( self.orderOnlyDependencyProductionAction )
        self.orderOnlyDependencyProductionAction.doPreview().returns( "create orderOnlyDependency" )

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( {
            "": {
                "": {},
                "create orderOnlyDependency": {},
            }
        } )
        self.assertTrue( Action.areSame( action, model ) )

    def getProductionActionAndPreview( self ):
        self.recordGetProductionActionPreview()

        self.m.startTest()

        action = self.artifact.getProductionAction()
        model = ActionModel.build( {
            "create file1": {
                "create dependency": {},
                "create orderOnlyDependency": {},
                "mkdir -p /tmp1": {},
                "rm -f /tmp1/file1": {}
            }
        } )
        self.assertTrue( Action.areSame( action, model ) )

    def recordGetProductionActionPreview( self ):
        self.artifact.doGetProductionAction().returns( self.productionAction )
        self.dependency.mustBeProduced().returns( True )
        self.dependency.computeProductionAction().returns( self.dependencyProductionAction )
        self.orderOnlyDependency.mustBeProduced().returns( True )
        self.orderOnlyDependency.computeProductionAction().returns( self.orderOnlyDependencyProductionAction )

        self.productionAction.doPreview().returns( "create file1" )
        with self.m.unorderedGroup():
            self.dependencyProductionAction.doPreview().returns( "create dependency" )
            self.orderOnlyDependencyProductionAction.doPreview().returns( "create orderOnlyDependency" )

    def testGetProductionActionWhenFileIsMissing( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( True )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenDependencyMustBeProduced( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
            self.dependency.mustBeProduced().returns( True )

        self.getProductionActionAndPreview()

    def testGetProductionActionWhenDependencyIsNewer( self ):
        for i in range( 2 ):
            AtomicArtifact._AtomicArtifact__fileIsMissing( "/tmp1/file1" ).returns( False )
            self.dependency.mustBeProduced().returns( False )
            self.artifact.getOldestFile().returns( 1200000 )
            self.dependency.getNewestFile().returns( 1200000 )

        self.getProductionActionAndPreview()

unittest.main()
