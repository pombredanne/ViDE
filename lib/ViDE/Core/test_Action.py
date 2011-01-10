from __future__ import with_statement

import unittest
import threading
import random
import os
import time

from Misc.MockMockMock import TestCase

from Action import Action, LongAction, CompoundException

class MyException( Exception ):
    pass

class ActionForMultiThreadTesting( Action ):
    lock = threading.Lock()

    def __init__( self, mgr, duration ):
        Action.__init__( self )
        self.__mgr = mgr
        self.__duration = duration

    def doExecute( self ):
        with ActionForMultiThreadTesting.lock:
            self.__mgr.begin( self )
        time.sleep( self.__duration )
        with ActionForMultiThreadTesting.lock:
            self.__mgr.end( self )

def isSuccessOrCanceled( a ):
    return a.isSuccess() or a.isCanceled()

class BasicAction( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a", Action )
        self.__oldTime = time.time

    def tearDown( self ):
        time.time = self.__oldTime
        TestCase.tearDown( self )

    def testExecute( self ):
        time.time = self.m.createMock( "time.time" )
        time.time().returns( 1 )
        self.a.doExecute()
        time.time().returns( 2 )

        self.m.startTest()
        self.a.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a.isSuccess() )
        self.assertEquals( self.a.getExecutionTimes(), ( 1, 2 ) )

    def testExecuteTwice( self ):
        self.a.doExecute()
        self.a.doExecute().raises( MyException( "Failure" ) )

        self.m.startTest()
        self.a.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a.isSuccess() )
        self.assertRaises( CompoundException, self.a.execute, keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a.isFailure() )

    def testFailure( self ):
        time.time = self.m.createMock( "time.time" )
        time.time().returns( 1 )
        self.a.doExecute().raises( MyException( "Failure" ) )
        time.time().returns( 2 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a.execute, keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a.isFailure() )
        self.assertEquals( self.a.getExecutionTimes(), ( 1, 2 ) )

    def testKeepGoing( self ):
        self.a.doExecute().raises( MyException( "Failure" ) )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a.execute, keepGoing = True, threadNumber = 1 )
        self.assertTrue( self.a.isFailure() )

    def testPreviewTwice( self ):
        self.a.doPreview().returns( "a's preview" )
        self.a.doPreview().returns( "a's preview" )

        self.m.startTest()
        self.assertEquals( self.a.preview(), [ "a's preview" ] )
        self.assertEquals( self.a.preview(), [ "a's preview" ] )

class DeepAction( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a1 = self.m.createMock( "self.a1", Action )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a3 = self.m.createMock( "self.a3", Action )
        self.a4 = self.m.createMock( "self.a4", Action )
        self.a2.addPredecessor( self.a1 )
        self.a3.addPredecessor( self.a2 )
        self.a4.addPredecessor( self.a3 )

    def testPredecessors( self ):
        self.assertTrue( self.a1 in self.a2.getPredecessors() )

    def testExecute( self ):
        self.a1.doExecute()
        self.a2.doExecute()
        self.a3.doExecute()
        self.a4.doExecute()

        self.m.startTest()
        self.a4.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a1.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isSuccess() )
        self.assertTrue( self.a4.isSuccess() )

    def testFailure( self ):
        self.a1.doExecute()
        self.a2.doExecute()
        self.a3.doExecute().raises( MyException( "Failure" ) )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a4.execute, keepGoing = False, threadNumber = 1  )
        self.assertTrue( self.a1.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isFailure() )
        self.assertTrue( self.a4.isFailure() )

    def testKeepGoing( self ):
        self.a1.doExecute()
        self.a2.doExecute()
        self.a3.doExecute().raises( MyException( "Failure" ) )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a4.execute, keepGoing = True, threadNumber = 1 )
        self.assertTrue( self.a1.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isFailure() )
        self.assertTrue( self.a4.isFailure() )

    def testPreview( self ):
        self.a1.doPreview().returns( "a1's preview" )
        self.a2.doPreview().returns( "a2's preview" )
        self.a3.doPreview().returns( "a3's preview" )
        self.a4.doPreview().returns( "a4's preview" )

        self.m.startTest()
        self.assertEquals( self.a4.preview(), [ "a1's preview", "a2's preview", "a3's preview", "a4's preview" ] )

class WideAction( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a11 = self.m.createMock( "self.a11", Action )
        self.a12 = self.m.createMock( "self.a12", Action )
        self.a13 = self.m.createMock( "self.a13", Action )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a2.addPredecessor( self.a11 )
        self.a2.addPredecessor( self.a12 )
        self.a2.addPredecessor( self.a13 )

    def testExecute( self ):
        with self.m.unorderedGroup():
            self.a11.doExecute()
            self.a12.doExecute()
            self.a13.doExecute()
        self.a2.doExecute()

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

    def testFailure( self ):
        with self.m.unorderedGroup():
            self.a11.doExecute().isOptional()
            self.a12.doExecute().raises( MyException( "Failure" ) )
            self.a13.doExecute().isOptional()

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = False, threadNumber = 1 )
        self.assertTrue( isSuccessOrCanceled( self.a11 ) )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( isSuccessOrCanceled( self.a13 ) )
        self.assertTrue( self.a2.isFailure() )

    def testKeepGoing( self ):
        with self.m.unorderedGroup():
            self.a11.doExecute()
            self.a12.doExecute().raises( MyException( "Failure" ) )
            self.a13.doExecute()

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = True, threadNumber = 1 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

    def testPreview( self ):
        with self.m.unorderedGroup():
            self.a11.doPreview().returns( "a11's preview" )
            self.a12.doPreview().returns( "a12's preview" )
            self.a13.doPreview().returns( "a13's preview" )
        self.a2.doPreview().returns( "a2's preview" )

        self.m.startTest()
        preview = self.a2.preview()
        self.assertEquals( len( preview ), 4 )
        self.assertEquals( set( preview[0:3] ), set( [ "a11's preview", "a12's preview", "a13's preview" ] ) )
        self.assertEquals( preview[3], "a2's preview" )

    def testEmptyPreview( self ):
        with self.m.unorderedGroup():
            self.a11.doPreview().returns( "a11's preview" )
            self.a12.doPreview().returns( "" )
            self.a13.doPreview().returns( "a13's preview" )
        self.a2.doPreview().returns( "a2's preview" )

        self.m.startTest()
        preview = self.a2.preview()
        self.assertEquals( len( preview ), 3 )
        self.assertEquals( set( preview[0:2] ), set( [ "a11's preview", "a13's preview" ] ) )
        self.assertEquals( preview[2], "a2's preview" )

class SeveralWaysAction( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a1 = self.m.createMock( "self.a1", Action )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a3 = self.m.createMock( "self.a3", Action )
        self.a3.addPredecessor( self.a2 )
        self.a3.addPredecessor( self.a1 )
        self.a2.addPredecessor( self.a1 )
        # a1 --> a2 --> a3
        #   \          /
        #    \---->---/

    def testExecute( self ):
        self.a1.doExecute()
        self.a2.doExecute()
        self.a3.doExecute()

        self.m.startTest()
        self.a3.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a1.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isSuccess() )

    def testPreview( self ):
        self.a1.doPreview().returns( "a1's preview" )
        self.a2.doPreview().returns( "a2's preview" )
        self.a3.doPreview().returns( "a3's preview" )

        self.m.startTest()
        self.assertEquals( self.a3.preview(), [ "a1's preview", "a2's preview", "a3's preview" ] )

class ExecuteLeavesFirst( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a1 = self.m.createMock( "self.a1", Action )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a3 = self.m.createMock( "self.a3", Action )
        self.a4 = self.m.createMock( "self.a4", Action )
        self.a5 = self.m.createMock( "self.a5", Action )
        self.a5.addPredecessor( self.a4 )
        self.a5.addPredecessor( self.a3 )
        self.a3.addPredecessor( self.a1 )
        self.a4.addPredecessor( self.a2 )

    def testExecute( self ):
        with self.m.unorderedGroup():
            self.a1.doExecute()
            self.a2.doExecute()
        with self.m.unorderedGroup():
            self.a3.doExecute()
            self.a4.doExecute()
        self.a5.doExecute()

        self.m.startTest()
        self.a5.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a1.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isSuccess() )
        self.assertTrue( self.a4.isSuccess() )
        self.assertTrue( self.a5.isSuccess() )

    def testFailure( self ):
        with self.m.unorderedGroup():
            self.a1.doExecute().raises( MyException( "Failure" ) )
            self.a2.doExecute().isOptional()

        self.m.startTest()
        self.assertRaises( CompoundException, self.a5.execute, keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a1.isFailure() )
        self.assertTrue( isSuccessOrCanceled( self.a2 ) )
        self.assertTrue( self.a3.isFailure() )
        self.assertTrue( self.a4.isCanceled() )
        self.assertEquals( self.a4.getExecutionTimes(), ( None, None ) )
        self.assertTrue( self.a5.isFailure() )

    def testKeepGoing( self ):
        with self.m.unorderedGroup():
            self.a1.doExecute().raises( MyException( "Failure" ) )
            self.a2.doExecute()
        self.a4.doExecute()

        self.m.startTest()
        self.assertRaises( CompoundException, self.a5.execute, keepGoing = True, threadNumber = 1 )
        self.assertTrue( self.a1.isFailure() )
        self.assertTrue( self.a2.isSuccess() )
        self.assertTrue( self.a3.isFailure() )
        self.assertTrue( self.a4.isSuccess() )
        self.assertTrue( self.a5.isFailure() )

    def testPreview( self ):
        with self.m.unorderedGroup():
            self.a1.doPreview().returns( "a1's preview" )
            self.a2.doPreview().returns( "a2's preview" )
        with self.m.unorderedGroup():
            self.a3.doPreview().returns( "a3's preview" )
            self.a4.doPreview().returns( "a4's preview" )
        self.a5.doPreview().returns( "a5's preview" )

        self.m.startTest()
        preview = self.a5.preview()
        self.assertEquals( set( preview[0:2] ), set( [ "a1's preview", "a2's preview" ] ) )
        self.assertEquals( set( preview[2:4] ), set( [ "a3's preview", "a4's preview" ] ) )
        self.assertEquals( preview[4], "a5's preview" )

class ExecuteLongActionsFirst( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a11 = self.m.createMock( "self.a11", LongAction )
        self.a12 = self.m.createMock( "self.a12", LongAction )
        self.a13 = self.m.createMock( "self.a13", LongAction )
        self.a14 = self.m.createMock( "self.a14", Action )
        self.a15 = self.m.createMock( "self.a15", Action )
        self.a11.getDuration = self.m.createMock( "self.a11.getDuration" )
        self.a12.getDuration = self.m.createMock( "self.a12.getDuration" )
        self.a13.getDuration = self.m.createMock( "self.a13.getDuration" )
        self.a11.doPreview = self.m.createMock( "self.a11.doPreview" )
        self.a12.doPreview = self.m.createMock( "self.a12.doPreview" )
        self.a13.doPreview = self.m.createMock( "self.a13.doPreview" )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a2.addPredecessor( self.a11 )
        self.a2.addPredecessor( self.a12 )
        self.a2.addPredecessor( self.a13 )
        self.a2.addPredecessor( self.a14 )
        self.a2.addPredecessor( self.a15 )
        
    def testExecute1( self ):
        with self.m.unorderedGroup():
            self.a12.getDuration().returns( 2 )
            self.a12.getDuration().returns( 2 ).isOptional()
            self.a11.getDuration().returns( 3 )
            self.a11.getDuration().returns( 3 ).isOptional()
            self.a13.getDuration().returns( 1 )
            self.a13.getDuration().returns( 1 ).isOptional()
        self.a11.doExecute()
        self.a11.doPreview().returns( "a11" )
        with self.m.unorderedGroup():
            self.a12.getDuration().returns( 2 )
            self.a12.getDuration().returns( 2 ).isOptional()
            self.a13.getDuration().returns( 1 )
            self.a13.getDuration().returns( 1 ).isOptional()
        self.a12.doExecute()
        self.a12.doPreview().returns( "a12" )
        self.a13.getDuration().returns( 1 )
        self.a13.getDuration().returns( 1 ).isOptional()
        self.a13.doExecute()
        self.a13.doPreview().returns( "a13" )
        with self.m.unorderedGroup():
            self.a14.doExecute()
            self.a15.doExecute()
        self.a2.doExecute()

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

    def testExecute2( self ):
        with self.m.unorderedGroup():
            self.a11.getDuration().returns( 1 )
            self.a11.getDuration().returns( 1 ).isOptional()
            self.a12.getDuration().returns( 3 )
            self.a12.getDuration().returns( 3 ).isOptional()
            self.a13.getDuration().returns( 2 )
            self.a13.getDuration().returns( 2 ).isOptional()
        self.a12.doExecute()
        self.a12.doPreview().returns( "a12" )
        with self.m.unorderedGroup():
            self.a11.getDuration().returns( 1 )
            self.a11.getDuration().returns( 1 ).isOptional()
            self.a13.getDuration().returns( 2 )
            self.a13.getDuration().returns( 2 ).isOptional()
        self.a13.doExecute()
        self.a13.doPreview().returns( "a13" )
        self.a11.getDuration().returns( 1 )
        self.a11.getDuration().returns( 1 ).isOptional()
        self.a11.doExecute()
        self.a11.doPreview().returns( "a11" )
        with self.m.unorderedGroup():
            self.a14.doExecute()
            self.a15.doExecute()
        self.a2.doExecute()

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 1 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

class DurationPickling( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a", LongAction )
        self.a.doPreview = self.m.createMock( "self.a.doPreview" )

    def test( self ):
        self.a.doPreview().returns( "a" )
    
        self.m.startTest()
        LongAction.dumpDurations()
        self.assertEquals( self.a.getDuration(), 0. )
        self.a.setDuration( 4. )
        self.assertEquals( self.a.getDuration(), 4. )
        self.a.setDuration( 1. )
        self.assertEquals( self.a.getDuration(), 2. )
        LongAction.dumpDurations()
        self.assertEquals( self.a.getDuration(), 0. )
        LongAction.loadDurations()
        self.assertEquals( self.a.getDuration(), 2. )

class Multithreading( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.mgr = self.m.createMock( "self.mgr" )
        self.a11 = ActionForMultiThreadTesting( self.mgr, ( 1 + random.random() ) / 10 )
        self.a12 = ActionForMultiThreadTesting( self.mgr, ( 1 + random.random() ) / 10 )
        self.a13 = ActionForMultiThreadTesting( self.mgr, ( 1 + random.random() ) / 10 )
        self.a14 = ActionForMultiThreadTesting( self.mgr, ( 1 + random.random() ) / 10 )
        self.a15 = ActionForMultiThreadTesting( self.mgr, ( 1 + random.random() ) / 10 )
        self.a2 = ActionForMultiThreadTesting( self.mgr, .1 )
        self.a2.addPredecessor( self.a11 )
        self.a2.addPredecessor( self.a12 )
        self.a2.addPredecessor( self.a13 )
        self.a2.addPredecessor( self.a14 )
        self.a2.addPredecessor( self.a15 )

    def testExecuteInTwoThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )
        self.mgr.begin( self.a2 )
        self.mgr.end( self.a2 )

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 2 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

    def testFailureInTwoThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 ).isOptional()
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 ).isOptional()
            self.mgr.begin( self.a14 ).isOptional()
            self.mgr.begin( self.a15 ).isOptional()
            self.mgr.end( self.a11 ).isOptional()
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 ).isOptional()
            self.mgr.end( self.a14 ).isOptional()
            self.mgr.end( self.a15 ).isOptional()

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = False, threadNumber = 2 )
        self.assertTrue( isSuccessOrCanceled( self.a11 ) )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( isSuccessOrCanceled( self.a13 ) )
        self.assertTrue( isSuccessOrCanceled( self.a14 ) )
        self.assertTrue( isSuccessOrCanceled( self.a15 ) )
        self.assertTrue( self.a2.isFailure() )

    def testKeepGoingInTwoThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = True, threadNumber = 2 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

    def testExecuteInFiveThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )
        self.mgr.begin( self.a2 )
        self.mgr.end( self.a2 )

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 5 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

    def testFailureInFiveThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = False, threadNumber = 5 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

    def testKeepGoingInFiveThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = True, threadNumber = 5 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

    def testExecuteInManyThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )
        self.mgr.begin( self.a2 )
        self.mgr.end( self.a2 )

        self.m.startTest()
        self.a2.execute( keepGoing = False, threadNumber = 10 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isSuccess() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isSuccess() )

    def testFailureInManyThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = False, threadNumber = 10 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

    def testKeepGoingInManyThreads( self ):
        with self.m.unorderedGroup():
            self.mgr.begin( self.a11 )
            self.mgr.begin( self.a12 )
            self.mgr.begin( self.a13 )
            self.mgr.begin( self.a14 )
            self.mgr.begin( self.a15 )
        with self.m.unorderedGroup():
            self.mgr.end( self.a11 )
            self.mgr.end( self.a12 ).raises( MyException( "Failure" ) )
            self.mgr.end( self.a13 )
            self.mgr.end( self.a14 )
            self.mgr.end( self.a15 )

        self.m.startTest()
        self.assertRaises( CompoundException, self.a2.execute, keepGoing = True, threadNumber = 10 )
        self.assertTrue( self.a11.isSuccess() )
        self.assertTrue( self.a12.isFailure() )
        self.assertTrue( self.a13.isSuccess() )
        self.assertTrue( self.a14.isSuccess() )
        self.assertTrue( self.a15.isSuccess() )
        self.assertTrue( self.a2.isFailure() )

class CompareActions( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a1 = self.m.createMock( "self.a1", Action )
        self.a2 = self.m.createMock( "self.a2", Action )
        self.a3 = self.m.createMock( "self.a3", Action )
        self.a4 = self.m.createMock( "self.a4", Action )
        self.b1 = self.m.createMock( "self.b1", Action )
        self.b2 = self.m.createMock( "self.b2", Action )
        self.b3 = self.m.createMock( "self.b3", Action )
        self.b4 = self.m.createMock( "self.b4", Action )

    def testDiffByPreview( self ):
        self.a4.doPreview().returns( "4" )
        self.b4.doPreview().returns( "four" )

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a4, self.b4 ) )

    def testDiffByPred( self ):
        self.a4.addPredecessor( self.a3 )

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a4, self.b4 ) )

    def makeDeep( self ):
        self.a2.addPredecessor( self.a1 )
        self.a3.addPredecessor( self.a2 )
        self.a4.addPredecessor( self.a3 )
        self.b2.addPredecessor( self.b1 )
        self.b3.addPredecessor( self.b2 )
        self.b4.addPredecessor( self.b3 )

    def testDeepEqual( self ):
        self.makeDeep()
        self.a4.doPreview().returns( "4" )
        self.a3.doPreview().returns( "3" )
        self.a2.doPreview().returns( "2" )
        self.a1.doPreview().returns( "1" )
        self.b4.doPreview().returns( "4" )
        self.b3.doPreview().returns( "3" )
        self.b2.doPreview().returns( "2" )
        self.b1.doPreview().returns( "1" )

        self.m.startTest()
        self.assertTrue( Action.areSame( self.a4, self.b4 ) )

    def testDeepDiffByPredPreview( self ):
        self.makeDeep()
        self.a4.doPreview().returns( "4" )
        self.a3.doPreview().returns( "3" )
        self.a2.doPreview().returns( "2" )
        self.a1.doPreview().returns( "1" )
        self.b4.doPreview().returns( "4" )
        self.b3.doPreview().returns( "three" )
        self.b2.doPreview().returns( "2" )
        self.b1.doPreview().returns( "1" )

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a4, self.b4 ) )

    def makeWide( self ):
        self.a4.addPredecessor( self.a1 )
        self.a4.addPredecessor( self.a2 )
        self.a4.addPredecessor( self.a3 )
        self.b4.addPredecessor( self.b1 )
        self.b4.addPredecessor( self.b2 )
        self.b4.addPredecessor( self.b3 )

    def testWideEqual( self ):
        self.makeWide()
        self.a4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.a3.doPreview().returns( "3" )
            self.a2.doPreview().returns( "2" )
            self.a1.doPreview().returns( "1" )
        self.b4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.b3.doPreview().returns( "3" )
            self.b2.doPreview().returns( "2" )
            self.b1.doPreview().returns( "1" )

        self.m.startTest()
        self.assertTrue( Action.areSame( self.a4, self.b4 ) )

    def testWideEqualInDifferentOrder( self ):
        self.makeWide()
        self.a4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.a3.doPreview().returns( "3" )
            self.a2.doPreview().returns( "2" )
            self.a1.doPreview().returns( "1" )
        self.b4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.b3.doPreview().returns( "2" )
            self.b2.doPreview().returns( "3" )
            self.b1.doPreview().returns( "1" )

        self.m.startTest()
        self.assertTrue( Action.areSame( self.a4, self.b4 ) )

    def testWideDiffByPredPreview( self ):
        self.makeWide()
        self.a4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.a3.doPreview().returns( "3" ).isOptional()
            self.a2.doPreview().returns( "2" )
            self.a1.doPreview().returns( "1" ).isOptional()
        self.b4.doPreview().returns( "4" )
        with self.m.unorderedGroup():
            self.b3.doPreview().returns( "3" ).isOptional()
            self.b2.doPreview().returns( "two" )
            self.b1.doPreview().returns( "1" ).isOptional()

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a4, self.b4 ) )

    def makeTwoWay( self ):
        self.a3.addPredecessor( self.a2 )
        self.a3.addPredecessor( self.a1 )
        self.a2.addPredecessor( self.a1 )
        ### @todo Exchange next two lines, to show a bug in Action.__haveSameStructure
        self.b3.addPredecessor( self.b2 )
        self.b3.addPredecessor( self.b1 )
        self.b2.addPredecessor( self.b1 )

    def testTwoWayEqual( self ):
        self.makeTwoWay()
        self.a3.doPreview().returns( "3" )
        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                self.a2.doPreview().returns( "2" )
                self.a1.doPreview().returns( "1" )
            self.a1.doPreview().returns( "1" )
        self.b3.doPreview().returns( "3" )
        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                self.b2.doPreview().returns( "2" )
                self.b1.doPreview().returns( "1" )
            self.b1.doPreview().returns( "1" )

        self.m.startTest()
        self.assertTrue( Action.areSame( self.a3, self.b3 ) )

    def testTwoWayDiffByPredPreview( self ):
        self.makeTwoWay()
        self.a3.doPreview().returns( "3" )
        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                self.a2.doPreview().returns( "2" )
                self.a1.doPreview().returns( "1" )
            self.a1.doPreview().returns( "1" )
        self.b3.doPreview().returns( "3" )
        with self.m.unorderedGroup():
            with self.m.orderedGroup():
                self.b2.doPreview().returns( "2" )
                self.b1.doPreview().returns( "one" )
            self.b1.doPreview().returns( "one" )

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a3, self.b3 ) )

    def testLookSameButDifferentStructureEqual( self ):
        self.a3.addPredecessor( self.a2 )
        self.a3.addPredecessor( self.a1 )
        self.a2.addPredecessor( self.a1 )
        self.b3.addPredecessor( self.b2 )
        self.b3.addPredecessor( self.b1 )
        self.b2.addPredecessor( self.b4 )

        self.m.startTest()
        self.assertFalse( Action.areSame( self.a3, self.b3 ) )

unittest.main()
