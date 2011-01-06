import math
import time
import itertools

import cairo

def segmentsIntersect( s1, s2 ):
    p11, p12 = s1
    p21, p22 = s2
    x11, y11 = p11
    x12, y12 = p12
    x21, y21 = p21
    x22, y22 = p22
    if max( [ x11, x12 ] ) < min( [ x21, x22 ] ):
        return False
    if max( [ x21, x22 ] ) < min( [ x11, x12 ] ):
        return False
    if max( [ y11, y12 ] ) < min( [ y21, y22 ] ):
        return False
    if max( [ y21, y22 ] ) < min( [ y11, y12 ] ):
        return False
    if ( ( y22 - y11 ) * ( x12 - x11 ) - ( x22 - x11 ) * ( y12 - y11 ) ) * ( ( y12 - y11 ) * ( x21 - x11 ) - ( y21 - y11 ) * ( x12 - x11 )  ) < 0:
        return False
    if ( ( y12 - y21 ) * ( x22 - x21 ) - ( x12 - x21 ) * ( y22 - y21 ) ) * ( ( y22 - y21 ) * ( x11 - x21 ) - ( y11 - y21 ) * ( x22 - x21 )  ) < 0:
        return False
    return True

def countSegmentIntersections( segments ):
    n = 0
    for s1 in segments: 
        for s2 in segments:
            if s1 is not s2:
                if segmentsIntersect( s1, s2 ):
                    n += 1
    return n

class ExecutionReport:
    HorizontalAxisHeight = 50
    PossibleGraduationIntervalDurations = [ 0.1, 0.5, 1, 5, 10, 15, 30, 60, 
                                            5 * 60, 10 * 60, 15 * 60, 30 * 60, 60 * 60,
                                            2 * 3600, 4 * 3600, 8 * 3600, 24 * 3600,
                                          ]

    class Action:
        def __init__( self, action ):
            self.begin, self.end = action.getExecutionTimes()
            self.success = action.isSuccess()
            self.text = action.doPreview()
            self.predecessors = set()

    ################################################################################ construction

    def __init__( self, action ):
        self.__actions = set()
        self.theBigMap = dict()
        self.__addAction( action )
        del self.theBigMap
        self.__computeDuration()

    def __addAction( self, action ):
        if action not in self.theBigMap:
            a = ExecutionReport.Action( action )
            self.theBigMap[ action ] = a
            self.__actions.add( a )
            for p in action.getPredecessors():
                self.__addAction( p )
                a.predecessors.add( self.theBigMap[ p ] )

    def __computeDuration( self ):
        begin = min( a.begin for a in self.__actions )
        for a in self.__actions:
            a.begin -= begin
            a.end -= begin
        self.__duration = max( a.end for a in self.__actions )

    ################################################################################ drawing (public interface)

    def draw( self, ctx, width, height ):
        self.ctx = ctx
        self.__pixelWidth = width
        self.__pixelHeight = height

        self.__computeCoordinates()
        ctx.save()
        self.__drawEveryThing()
        ctx.restore()

    ################################################################################ computation of coordinates

    def __computeCoordinates( self ):
        self.__computeAbscissa()
        self.__computeOrdinates()

    def __computeOrdinates( self ):
        bestOrdering = list( self.__actions )
        bestOrderingCost = self.__evaluateOrdering( bestOrdering )
        for ordering in itertools.permutations( self.__actions ):
            orderingCost = self.__evaluateOrdering( ordering )
            if orderingCost < bestOrderingCost:
                bestOrderingCost = orderingCost
                bestOrdering = ordering
        self.__applyActionOrdering( bestOrdering )
        self.__horizontalAxisOrdinate = 25

    def __applyActionOrdering( self, ordering ):
        for i, a in enumerate( ordering ):
            a.y = i * 20 + 50

    def __evaluateOrdering( self, ordering ):
        self.__applyActionOrdering( ordering )
        return ( self.__countCrossings(), self.__countLinksGoingUp() )

    def __countCrossings( self ):
        segments = set()
        for a in self.__actions:
            segments.add( ( ( a.begin, a.y ), ( a.end, a.y ) ) )
            for p in a.predecessors:
                segments.add( ( ( p.end, p.y ), ( a.begin, a.y ) ) )
        return countSegmentIntersections( segments )

    def __countLinksGoingUp( self ):
        n = 0
        for a in self.__actions:
            for p in a.predecessors:
                if p.y > a.y:
                    n += 1
        return n

    def __computeAbscissa( self ):
        self.__computeOptimalTranscale()
        self.__computeGraduations()

    def __computeOptimalTranscale( self ):
        self.__pixelForZero = self.__textWidth( self.__graduationLabel( 0. ) ) / 2

        self.__optimalHorizontalScale = ( self.__pixelWidth - self.__pixelForZero ) / self.__duration
        for a in self.__actions:
            if a.begin != 0:
                maximumScaleForA = ( self.__pixelWidth - self.__pixelForZero - self.__textWidth( a.text ) ) / a.begin
                if maximumScaleForA < self.__optimalHorizontalScale:
                    self.__optimalHorizontalScale = maximumScaleForA

    def __textWidth( self, a ):
        x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents( a )
        return width

    def __computeGraduations( self ):
        for intervalDuration in ExecutionReport.PossibleGraduationIntervalDurations:
            if self.__tryIntervalDuration( intervalDuration ):
                break

    def __tryIntervalDuration( self, intervalDuration ):
        if self.__duration >= 10 and intervalDuration < 1:
            return False
        numberOfIntervals = int( math.ceil( self.__duration / intervalDuration ) )
        self.__graduationPoints = [ i * intervalDuration for i in range( numberOfIntervals + 1 ) ]
        lastLabelWidth = self.__textWidth( self.__graduationLabel( self.__graduationPoints[-1] ) )
        self.__horizontalScale = min( [
            self.__optimalHorizontalScale,
            ( self.__pixelWidth - self.__pixelForZero - lastLabelWidth / 2 ) / self.__graduationPoints[-1]
        ] )
        firstLabelWidth = self.__textWidth( self.__graduationLabel( 0. ) )
        minimalWidthOfAllIntervals = 2 * numberOfIntervals * firstLabelWidth
        actualWidthOfAllIntervals = self.__horizontalScale * self.__graduationPoints[-1]
        return minimalWidthOfAllIntervals <= actualWidthOfAllIntervals

    def __graduationLabel( self, t ):
        if self.__duration >= 3600:
            return time.strftime( "%H:%M:%S", time.gmtime( t ) )
        elif self.__duration >= 60:
            return time.strftime( "%M:%S", time.gmtime( t ) )
        elif self.__duration >= 10:
            return str( int( t ) )
        else:
            return "%.1f" % t

    ################################################################################ drawing

    def __drawEveryThing( self ):
        self.__drawBackground()
        self.__drawHorizontalAxis()
        self.__drawLinks()
        self.__drawActions()

    def __drawBackground( self ):
        self.ctx.set_source_rgb( 1, 1, 1 )
        self.ctx.rectangle( 0, 0, self.__pixelWidth, self.__pixelHeight )
        self.ctx.fill()

    def __drawHorizontalAxis( self ):
        self.__drawAxis()
        self.ctx.translate( self.__pixelForZero, 0 )
        self.ctx.scale( self.__horizontalScale, 1 )
        self.__drawGraduations()

    def __drawAxis( self ):
        self.ctx.set_source_rgb( 0, 0, 0 )
        self.ctx.move_to( 0, self.__horizontalAxisOrdinate )
        self.ctx.line_to( self.__pixelForZero + self.__horizontalScale * self.__graduationPoints[ -1 ] + self.__textWidth( self.__graduationLabel( self.__graduationPoints[ -1 ] ) ) / 2, self.__horizontalAxisOrdinate )
        self.ctx.stroke()

    def __drawGraduations( self ):
        for t in self.__graduationPoints:
            self.__drawGraduation( t )

    def __drawGraduation( self, t ):
        self.ctx.set_line_width( 2 )
        self.ctx.move_to( t, self.__horizontalAxisOrdinate - 5 )
        self.ctx.line_to( t, self.__horizontalAxisOrdinate + 5 )
        self.ctx.save()
        self.ctx.identity_matrix()
        self.ctx.stroke()
        self.ctx.restore()
        self.ctx.move_to( t, self.__horizontalAxisOrdinate - 6 )
        self.ctx.save()
        self.ctx.identity_matrix()
        label = self.__graduationLabel( t )
        x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents( label )
        self.ctx.rel_move_to( -width / 2 - x_bearing, 0 )
        self.ctx.show_text( label )
        self.ctx.restore()

    def __drawLinks( self ):
        self.ctx.set_source_rgb( .7, .7, .7 )
        self.ctx.set_line_width( 1 )
        for a in self.__actions:
            for p in a.predecessors:
                self.__drawLink( p, a )

    def __drawLink( self, p, a ):
        self.ctx.move_to( p.end, p.y )
        self.ctx.line_to( a.begin, a.y )
        self.ctx.save()
        self.ctx.identity_matrix()
        #self.ctx.set_antialias( cairo.ANTIALIAS_NONE )
        self.ctx.stroke()
        self.ctx.restore()

    def __drawActions( self ):
        self.ctx.set_line_width( 4 )
        for a in self.__actions:
            self.__drawAction( a )

    def __drawAction( self, a ):
        self.ctx.move_to( a.begin, a.y )
        self.ctx.line_to( a.end, a.y )
        self.ctx.save()
        self.__setColorForAction( a )
        self.ctx.identity_matrix()
        self.ctx.stroke()
        self.ctx.restore()
        self.ctx.move_to( a.begin, a.y - 5 )
        self.ctx.save()
        self.ctx.set_source_rgb( 0, 0, 0 )
        self.ctx.identity_matrix()
        self.ctx.show_text( a.text )
        self.ctx.restore()

    def __setColorForAction( self, a ):
        if a.success:
            self.ctx.set_source_rgb( 0, 0, 1 )
        else:
            self.ctx.set_source_rgb( 1, 0, 0 )

