#!/usr/bin/env python

from __future__ import with_statement

import unittest

from MockMockMock import TestCase, UnexpectedCall, ExpectedMoreCalls

class ToBeMocked:
    def __init__( self ):
        pass

class MyException( Exception ):
    pass

class TestReturnValue( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a().returns( 42 )
        self.m.startTest()

    def test( self ):
        self.assertEquals( self.o.a(), 42 )

class TestRaiseException( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a().raises( MyException() )
        self.m.startTest()

    def test( self ):
        self.assertRaises( MyException, self.o.a )

class TestCheckCall( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o1 = self.m.createMock( "self.o1", ToBeMocked )
        self.o2 = self.m.createMock( "self.o2", ToBeMocked )
        self.o1.foobar( "abc", "def" )
        self.o2.foobar( "abc", "def" )
        self.o1.baz()
        self.m.startTest()

    def testOk( self ):
        self.o1.foobar( "abc", "def" )
        self.o2.foobar( "abc", "def" )
        self.o1.baz()

    def testBadObject( self ):
        self.assertRaises( UnexpectedCall, self.o2.foobar, "abc", "def" )

    def testBadMethod( self ):
        self.assertRaises( UnexpectedCall, self.o1.baz, "abc", "def" )

    def testBadArguments( self ):
        self.assertRaises( UnexpectedCall, self.o1.foobar, "abc", "ghi" )

class TestOrderedGroup:
    def testGoodOrder( self ):
        self.o.a()
        self.o.b()
        self.o.c()

    def testBadOrder1( self ):
        self.assertRaises( UnexpectedCall, self.o.b )

    def testBadOrder2( self ):
        self.assertRaises( UnexpectedCall, self.o.c )

    def testBadOrder3( self ):
        self.o.a()
        self.assertRaises( UnexpectedCall, self.o.c )

    def testExpectingMoreCalls( self ):
        self.o.a()
        self.o.b()
        self.assertRaises( ExpectedMoreCalls, self.m.endTest )

    def testExpectingLessCalls( self ):
        self.o.a()
        self.o.b()
        self.o.c()
        self.assertRaises( UnexpectedCall, self.o.a )

class TestSimpleOrderedGroup( TestCase, TestOrderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a()
        with self.m.orderedGroup():
            self.o.b()
        self.o.c()
        self.m.startTest()

class TestJustLessSimpleOrderedGroup( TestCase, TestOrderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a()
        with self.m.orderedGroup():
            self.o.b()
            self.o.c()
        self.m.startTest()

class TestDeepOrderedGroup( TestCase, TestOrderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        with self.m.orderedGroup():
            self.o.a()
            with self.m.orderedGroup():
                self.o.b()
                with self.m.orderedGroup():
                    self.o.c()
        self.m.startTest()

class TestUnorderedGroup:
    def testGoodOrder1( self ):
        self.o.a()
        self.o.b()
        self.o.c()
        self.o.d()

    def testGoodOrder2( self ):
        self.o.a()
        self.o.b()
        self.o.d()
        self.o.c()

    def testGoodOrder3( self ):
        self.o.a()
        self.o.c()
        self.o.b()
        self.o.d()

    def testGoodOrder4( self ):
        self.o.a()
        self.o.c()
        self.o.d()
        self.o.b()

    def testGoodOrder5( self ):
        self.o.b()
        self.o.d()
        self.o.a()
        self.o.c()

    def testExpectingMoreCalls( self ):
        self.o.a()
        self.o.b()
        self.assertRaises( ExpectedMoreCalls, self.m.endTest )

    def testExpectingLessCalls( self ):
        self.o.a()
        self.o.b()
        self.o.c()
        self.o.d()
        self.assertRaises( UnexpectedCall, self.o.a )

class TestSimpleUnorderedGroup( TestCase, TestUnorderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        with self.m.unorderedGroup():
            self.o.a()
            self.o.b()
            self.o.c()
            self.o.d()
        self.m.startTest()

class TestJustLessSimpleUnorderedGroup( TestCase, TestUnorderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        with self.m.unorderedGroup():
            self.o.a()
            with self.m.unorderedGroup():
                self.o.b()
                self.o.c()
            self.o.d()
        self.m.startTest()

class TestDeepUnorderedGroup( TestCase, TestUnorderedGroup ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        with self.m.unorderedGroup():
            self.o.a()
            with self.m.unorderedGroup():
                self.o.b()
                with self.m.unorderedGroup():
                    self.o.c()
                    with self.m.unorderedGroup():
                        self.o.d()
        self.m.startTest()

class TestAnyOrder( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a()
        self.o.b()
        with self.m.unorderedGroup():
            self.o.c1()
            with self.m.orderedGroup():
                self.o.d()
                self.o.e()
            self.o.c2()
            self.o.c3()
        self.o.f()
        self.o.g()
        self.m.startTest()

    def test1( self ):
        self.o.a()
        self.o.b()
        self.o.c1()
        self.o.d()
        self.o.e()
        self.o.c2()
        self.o.c3()
        self.o.f()
        self.o.g()

    def test2( self ):
        self.o.a()
        self.o.b()
        self.o.d()
        self.o.e()
        self.o.c3()
        self.o.c2()
        self.o.c1()
        self.o.f()
        self.o.g()

    def test3( self ):
        self.o.a()
        self.o.b()
        self.assertRaises( UnexpectedCall, self.o.e )

    def test4( self ):
        self.o.a()
        self.o.b()
        self.o.c3()
        self.assertRaises( UnexpectedCall, self.o.e )

class TestOptionalInOrderedGroup( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        self.o.a()
        self.o.b().isOptional()
        self.o.c()
        self.m.startTest()

    def testCallOptional( self ):
        self.o.a()
        self.o.b()
        self.o.c()

    def testDontCallOptional( self ):
        self.o.a()
        self.o.c()

class TestOptionalInUnorderedGroup( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.o = self.m.createMock( "self.o", ToBeMocked )
        with self.m.unorderedGroup():
            self.o.a()
            self.o.b().isOptional()
            self.o.c()
        self.m.startTest()

    def testCallOptional( self ):
        self.o.b()
        self.o.a()
        self.o.c()

    def testDontCallOptional( self ):
        self.o.c()
        self.o.a()

class TestOrderedGroupInUnorderedGroup( TestCase ):
    pass

class TestUnorderedGroupInOrderedGroup( TestCase ):
    pass

unittest.main()
