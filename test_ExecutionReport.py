#!/usr/bin/env python

from __future__ import with_statement

import unittest
import struct
import random

import cairo

from MockMockMock import TestCase

from ExecutionReport import ExecutionReport, segmentsIntersect

class SegmentIntersection( TestCase ):
    def test( self ):
        img = cairo.ImageSurface( cairo.FORMAT_RGB24, 800, 800 )
        ctx = cairo.Context( img )
        ctx.set_source_rgb( .9, .9, .9 )
        ctx.paint()
        ctx.set_line_width( 1 )
        ctx.set_antialias( cairo.ANTIALIAS_NONE )
        
        s = ( ( random.randint( 200, 600 ), random.randint( 200, 600 ) ), ( random.randint( 200, 600 ), random.randint( 200, 600 ) ) )
        coords = range( 0, 900, 200 )
        ctx.set_source_rgb( 1, 0, 0 )
        for x1 in coords:
            for y1 in coords:
                for x2 in coords:
                    for y2 in coords:
                        s2 = ( ( x1, y1 ), ( x2, y2 ) )
                        self.pathSegment( ctx, s2 )
        ctx.stroke()
        ctx.set_source_rgb( 0, 1, 0 )
        for x1 in coords:
            for y1 in coords:
                for x2 in coords:
                    for y2 in coords:
                        s2 = ( ( x1, y1 ), ( x2, y2 ) )
                        if segmentsIntersect( s, s2 ):
                            self.pathSegment( ctx, s2 )
        ctx.stroke()
        ctx.set_source_rgb( 0, 0, 1 )
        self.pathSegment( ctx, s )
        ctx.stroke()

        img.write_to_png( "SegmentIntersection.png" )

    def pathSegment( self, ctx, s ):
        p1, p2 = s
        x1, y1 = p1
        x2, y2 = p2
        ctx.move_to( x1, y1 )
        ctx.line_to( x2, y2 )

class DrawSomething( TestCase ):
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a" )
        self.b = self.m.createMock( "self.b" )
        self.c = self.m.createMock( "self.c" )
        self.d = self.m.createMock( "self.d" )
        self.e = self.m.createMock( "self.e" )

    def test( self ):
        with self.m.unorderedGroup():
            self.a.getExecutionTimes().returns( ( 115., 119. ) )
            self.a.isSuccess().returns( False )
            self.a.doPreview().returns( "self.a's preview" )
            self.a.getPredecessors().returns( [ self.b, self.d ] )
            self.b.getExecutionTimes().returns( ( 69., 90. ) )
            self.b.isSuccess().returns( True )
            self.b.doPreview().returns( "self.b's preview" )
            self.b.getPredecessors().returns( [ self.c, self.e ] )
            self.c.getExecutionTimes().returns( ( 0., 38. ) )
            self.c.isSuccess().returns( True )
            self.c.doPreview().returns( "self.c's preview" )
            self.c.getPredecessors().returns( [] )
            self.d.getExecutionTimes().returns( ( 59., 109. ) )
            self.d.isSuccess().returns( True )
            self.d.doPreview().returns( "self.d's preview" )
            self.d.getPredecessors().returns( [ self.e ] )
            self.e.getExecutionTimes().returns( ( 0., 58. ) )
            self.e.isSuccess().returns( True )
            self.e.doPreview().returns( "self.e's preview" )
            self.e.getPredecessors().returns( [] )

        self.m.startTest()

        report = ExecutionReport( self.a )
        img = cairo.ImageSurface( cairo.FORMAT_RGB24, 800, 600 )
        ctx = cairo.Context( img )
        ctx.translate( 10, 10 )
        ctx.set_source_rgb( .9, .9, .9 )
        ctx.paint()
        report.draw( ctx, 780, 580 )
        img.write_to_png( "test_ExecutionReport.png" )
        
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
        self.a.doPreview().returns( "self.a's preview" )
        self.a.getPredecessors().returns( [] )

        self.m.startTest()

        report = ExecutionReport( self.a )
        img = cairo.ImageSurface( cairo.FORMAT_RGB24, 1, 1 )
        ctx = cairo.Context( img )
        report.draw( ctx, width, 100 )

        graduations = [ report._ExecutionReport__graduationLabel( g ) for g in report._ExecutionReport__graduationPoints ]
        previousGraduation = None
        for graduation in graduations:
            self.assertNotEqual( graduation, previousGraduation )
            previousGraduation = graduation

class HorizontalMargins( TestCase, TestCaseWithDurationsAndWidths( [ 0.1, 0.9, 1.0, 1.1, 55, 60, 65, 7000, 7200, 7400 ], range( 230, 800, 25 ) ) ):
    """Drawings have exactly the requested width"""
    def setUp( self ):
        TestCase.setUp( self )
        self.a = self.m.createMock( "self.a" )
        self.b = self.m.createMock( "self.b" )
        self.c = self.m.createMock( "self.c" )

    def performTest( self, duration, width, testName ):
        self.a.getExecutionTimes().returns( ( .7 * duration, 1. * duration ) )
        self.a.isSuccess().returns( True )
        self.a.doPreview().returns( "self.a's preview" )
        self.a.getPredecessors().returns( [ self.b ] )
        self.b.getExecutionTimes().returns( ( .3 * duration, .4 * duration ) )
        self.b.isSuccess().returns( True )
        self.b.doPreview().returns( "self.b's preview, a bit longer than others" )
        self.b.getPredecessors().returns( [ self.c ] )
        self.c.getExecutionTimes().returns( ( .0, .2 * duration ) )
        self.c.isSuccess().returns( True )
        self.c.doPreview().returns( "self.c's preview" )
        self.c.getPredecessors().returns( [] )

        self.m.startTest()
        report = ExecutionReport( self.a )

        marginSize = 10
        height = 100
        img = cairo.ImageSurface( cairo.FORMAT_ARGB32, width + 2 * marginSize, height + 2 * marginSize )
        ctx = cairo.Context( img )
        ctx.set_source_rgb( 1, 1, 1 )
        ctx.paint()
        report.draw( ctx, width, height )
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
        if not reason == "":
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
