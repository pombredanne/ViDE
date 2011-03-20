from __future__ import with_statement

import unittest
import struct

import cairo

from Misc.MockMockMock import TestCase

from ExecutionReport import ExecutionReport

class Ordinates( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a" )
        self.b = self.m.createMock( "self.b" )
        self.c = self.m.createMock( "self.c" )
        self.d = self.m.createMock( "self.d" )

    def testOneBranch( self ):
        self.d.getExecutionTimes().returns( ( 3., 4. ) )
        self.d.isSuccess().returns( True )
        self.d.getPreview().returns( "d" )
        self.d.getPredecessors().returns( [ self.c ] )
        self.c.getExecutionTimes().returns( ( 2., 3. ) )
        self.c.isSuccess().returns( True )
        self.c.getPreview().returns( "c" )
        self.c.getPredecessors().returns( [ self.b ] )
        self.b.getExecutionTimes().returns( ( 1., 2. ) )
        self.b.isSuccess().returns( True )
        self.b.getPreview().returns( "b" )
        self.b.getPredecessors().returns( [ self.a ] )
        self.a.getExecutionTimes().returns( ( 0., 1. ) )
        self.a.isSuccess().returns( True )
        self.a.getPreview().returns( "a" )
        self.a.getPredecessors().returns( [] )

        self.m.startTest()

        report = ExecutionReport( self.d, 800 )
        for action in report._ExecutionReport__actions:
            if action.text == "a":
                self.assertEqual( action.y, 45 )
            if action.text == "b":
                self.assertEqual( action.y, 65 )
            if action.text == "c":
                self.assertEqual( action.y, 85 )
            if action.text == "d":
                self.assertEqual( action.y, 105 )

    def testTwoBranches( self ):
        self.d.getExecutionTimes().returns( ( 3., 4. ) )
        self.d.isSuccess().returns( True )
        self.d.getPreview().returns( "d" )
        self.d.getPredecessors().returns( [ self.c, self.b ] )
        self.c.getExecutionTimes().returns( ( 2., 3. ) )
        self.c.isSuccess().returns( True )
        self.c.getPreview().returns( "c" )
        self.c.getPredecessors().returns( [ self.a ] )
        self.a.getExecutionTimes().returns( ( 0., 1. ) )
        self.a.isSuccess().returns( True )
        self.a.getPreview().returns( "a" )
        self.a.getPredecessors().returns( [] )
        self.b.getExecutionTimes().returns( ( 1., 2. ) )
        self.b.isSuccess().returns( True )
        self.b.getPreview().returns( "b" )
        self.b.getPredecessors().returns( [ self.a ] )

        self.m.startTest()

        report = ExecutionReport( self.d, 800 )
        for action in report._ExecutionReport__actions:
            if action.text == "a":
                self.assertEqual( action.y, 45 )
            if action.text == "b":
                self.assertEqual( action.y, 85 )
            if action.text == "c":
                self.assertEqual( action.y, 65 )
            if action.text == "d":
                self.assertEqual( action.y, 105 )

def TestCaseWithDurationsAndWidths( durations, widths ):
    class TheNewClass:
        pass
    def addTest( d, w, n ): # Needed for closure purpose: d, w, and n must be local variables to be used in lambda
        setattr( TheNewClass, "test_" + n, lambda self: self.performTest( float( d ), w, n ) )
    def durationString( duration ):
        if isinstance( duration, int ):
            return str( duration ) + "sec"
        else:
            return str( duration ).replace( ".", "sec" )
    def testName( duration, width ):
        return durationString( duration ) + "_" + str( width ) + "px"
    for duration in durations :
        for width in widths:
            addTest( duration, width, testName( duration, width ) )
    return TheNewClass
    
class GraduationLabels( TestCase, TestCaseWithDurationsAndWidths( [ 0.1, 0.9, 1.0, 1.1, 9, 10, 11, 55, 60, 65, 7000, 7200, 7400 ], [ 200, 50000 ] ) ):
    """Label texts are never duplicated"""
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a" )

    def performTest( self, duration, width, testName ):
        self.a.getExecutionTimes().returns( ( 0., 1. * duration ) )
        self.a.isSuccess().returns( True )
        self.a.getPreview().returns( "self.a's preview" )
        self.a.getPredecessors().returns( [] )

        self.m.startTest()

        report = ExecutionReport( self.a, width )
        img = cairo.ImageSurface( cairo.FORMAT_RGB24, 1, 1 )
        ctx = cairo.Context( img )
        report.draw( ctx )

        graduations = [ report._ExecutionReport__graduationLabel( g ) for g in report._ExecutionReport__graduationPoints ]
        previousGraduation = None
        for graduation in graduations:
            self.assertNotEqual( graduation, previousGraduation )
            previousGraduation = graduation

class HorizontalMargins( TestCase, TestCaseWithDurationsAndWidths( [ 0.1, 0.9, 1.0, 1.1, 55, 60, 65, 7000, 7200, 7400 ], range( 255, 800, 25 ) ) ):
    """Drawings have exactly the requested width"""
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a" )
        self.b = self.m.createMock( "self.b" )
        self.c = self.m.createMock( "self.c" )

    def performTest( self, duration, width, testName ):
        self.a.getExecutionTimes().returns( ( .7 * duration, 1. * duration ) )
        self.a.isSuccess().returns( True )
        self.a.getPreview().returns( "self.a's preview" )
        self.a.getPredecessors().returns( [ self.b ] )
        self.b.getExecutionTimes().returns( ( .3 * duration, .4 * duration ) )
        self.b.isSuccess().returns( True )
        self.b.getPreview().returns( "self.b's preview, a bit longer than others" )
        self.b.getPredecessors().returns( [ self.c ] )
        self.c.getExecutionTimes().returns( ( .0, .2 * duration ) )
        self.c.isSuccess().returns( True )
        self.c.getPreview().returns( "self.c's preview" )
        self.c.getPredecessors().returns( [] )

        self.m.startTest()
        report = ExecutionReport( self.a, width + 20 )

        marginSize = 10
        height = 100
        img = cairo.ImageSurface( cairo.FORMAT_ARGB32, width + 2 * marginSize, height + 2 * marginSize )
        ctx = cairo.Context( img )
        ctx.set_source_rgb( 1, 1, 1 )
        ctx.paint()
        ctx.translate( marginSize, marginSize )
        report.draw( ctx )
        leftMarginIsWhite, rightMarginIsWhite, drawingTouchesLeft, drawingTouchesRight = self.checkHorizontalMargins( img, marginSize, 0xFFFFFFFF )
        reason = ""
        if not leftMarginIsWhite:
            reason += ".spreads_on_left_margin"
        if not rightMarginIsWhite:
            reason += ".spreads_on_right_margin"
        if not drawingTouchesLeft:
            reason += ".far_from_left"
        if not drawingTouchesRight:
            reason += ".far_from_right"
        if reason != "":
            img.write_to_png( "HorizontalMargins." + testName + reason + ".png" )
        self.assertTrue( leftMarginIsWhite )
        self.assertTrue( rightMarginIsWhite )
        self.assertTrue( drawingTouchesLeft )
        self.assertTrue( drawingTouchesRight )

    def checkHorizontalMargins( self, img, marginSize, marginColor ):
        stride = img.get_stride()
        width = img.get_width()
        height = img.get_height()
        data = img.get_data()
        leftMarginIsWhite = True
        rightMarginIsWhite = True
        drawingTouchesLeft = False
        drawingTouchesRight = False
        for y in range( height ):
            for x in range( marginSize ):
                leftMarginIsWhite = leftMarginIsWhite and struct.unpack_from( 'I', data, y * stride + x * 4 ) == (marginColor,)
                rightMarginIsWhite = rightMarginIsWhite and struct.unpack_from( 'I', data, y * stride + ( width - x - 1 ) * 4 ) == (marginColor,)
            drawingTouchesLeft = drawingTouchesLeft or struct.unpack_from( 'I', data, y * stride + marginSize * 4 ) != (marginColor,)
            drawingTouchesRight = drawingTouchesRight or struct.unpack_from( 'I', data, y * stride + ( width - marginSize - 1 ) * 4 ) != (marginColor,)
        return leftMarginIsWhite, rightMarginIsWhite, drawingTouchesLeft, drawingTouchesRight

unittest.main()
