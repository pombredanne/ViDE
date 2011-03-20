from __future__ import with_statement

import multiprocessing
import threading
import time

from Misc import Graphviz

from ViDE import Log
from ViDE.Core.CallOnceAndCache import CallOnceAndCache

class CompoundException( Exception ):
    def __init__( self, exceptions ):
        self.__exceptions = exceptions

    def __str__( self ):
        return "CompoundException( [" + ", ".join( str( e ) for e in self.__exceptions ) + "] )"

class Action( CallOnceAndCache ):
    ###################################################################### virtuals to be implemented
    # doExecute
    # computePreview

    ###################################################################### construction

    def __init__( self ):
        CallOnceAndCache.__init__( self )
        self.__predecessors = set()
        self.__previewed = False
        self.__executionState = Action.__Initial()
        self.__executionBegin = None
        self.__executionEnd = None

    def addPredecessor( self, p ):
        self.__predecessors.add( p )

    def getPredecessors( self ):
        return self.__predecessors

    def getAllPredecessors( self ):
        predecessors = set()
        predecessors.update( self.__predecessors )
        for p in self.__predecessors:
            predecessors.update( p.getAllPredecessors() )
        return predecessors
        
    ###################################################################### height-based accessors

    def __getLowestPredecessorMatchingCriteria( self, criteria ):
        predecessors = self.__getLowestPredecessorsMatchingCriteria( criteria )
        if len( predecessors ) != 0:
            return predecessors[ 0 ]
        else:
            return None
    
    def __getLowestPredecessorsMatchingCriteria( self, criteria ):
        next = [ self ]
        for p in self.__predecessors:
            n = p.__getLowestPredecessorsMatchingCriteria( criteria )
            if len( n ) != 0:
                if n[ 0 ].__height() < next[ 0 ].__height():
                    next = n
                if n[ 0 ].__height() == next[ 0 ].__height():
                    next += n
        return [ n for n in next if criteria( n ) ]

    def __height( self ):
        if len( self.__predecessors ) == 0:
            return 0
        return max( p.__height() for p in self.__predecessors ) + 1

    ###################################################################### preview

    def preview( self ):
        return self.__preview()

    def getPreview( self ):
        return self.getCached( "preview", self.computePreview )
        
    def __preview( self ):
        preview = []
        while True:
            next = self.__getNextToPreview()
            if next is None:
                break
            next.__previewed = True
            text = next.getPreview()
            if text != "":
                preview.append( text )
        return preview

    def __getNextToPreview( self ):
        return self.__getLowestPredecessorMatchingCriteria( lambda a: not a.__previewed )

    ###################################################################### graph

    def getGraph( self ):
        g = Graphviz.Graph( "action" )
        g.nodeAttr[ "shape" ] = "box"
        for element in self.__getGraphElements():
            g.add( element )
        return g
    
    def __getGraphNode( self ):
        return self.getCached( "graphNode", lambda: Graphviz.Node( self.getPreview() ) )
    
    def __getGraphElements( self ):
        return self.getCached( "graphElements", self.computeGraphElements )

    def computeGraphElements( self ):
        graphElements = [ self.__getGraphNode() ]
        for predecessor in self.__predecessors:
            graphElements += predecessor.__getGraphElements()
            graphElements.append( Graphviz.Link( self.__getGraphNode(), predecessor.__getGraphNode() ) )
        return graphElements

    ###################################################################### execution state

    class __ExecutionState:
        def isInitial( self ): return False
        def isEnded( self ): return False
        def isSuccess( self ): return False
        def isFailure( self ): return False
        def isCanceled( self ): return False
    class __Initial( __ExecutionState ):
        def isInitial( self ): return True
    class __Executing( __ExecutionState ):
        pass
    class __Ended( __ExecutionState ):
        def isEnded( self ): return True
    class __Success( __Ended ):
        def isSuccess( self ): return True
    class __Failure( __Ended ):
        def isFailure( self ): return True
    class __Canceled( __Ended ):
        def isCanceled( self ): return True

    def isInitial( self ): return self.__executionState.isInitial()
    def isEnded( self ): return self.__executionState.isEnded()
    def isSuccess( self ): return self.__executionState.isSuccess()
    def isFailure( self ): return self.__executionState.isFailure()
    def isCanceled( self ): return self.__executionState.isCanceled()

    def getExecutionTimes( self ):
        return self.__executionBegin, self.__executionEnd
        
    ###################################################################### execute

    def execute( self, keepGoing, threadNumber ):
        if threadNumber == -1:
            try:
                threadNumber = multiprocessing.cpu_count() + 1
            except NotImplementedError:
                threadNumber = 2
            Log.verbose( "Automatically using", threadNumber, "jobs" )
        self.__prepareExecution()
        self.__executeInThreads( keepGoing, threadNumber )
        self.__checkExecution()

    def __prepareExecution( self ):
        self.__exceptions = []
        self.cond = threading.Condition()

    def __checkExecution( self ):
        del self.cond
        if len( self.__exceptions ) != 0:
            raise CompoundException( self.__exceptions )

    def __executeInThreads( self, keepGoing, threadNumber ):
        # @todo Do not create all threads at the begining, but only when needed.
        # This will allow the "make -j" (without jobs count) behavior:
        # create as many threads as needed to parallelize every actions
        # This will also allow to execute short actions in the main thread
        threads = []
        for i in range( threadNumber ):
            thread = threading.Thread( target = lambda: self.__executeInOneThread( keepGoing ) )
            thread.start()
            threads.append( thread )
        for thread in threads:
            thread.join()

    def __executeInOneThread( self, keepGoing ):
        while True:
            with self.cond:
                a = self.__waitUntilNextPotentialExecutable()
                if a is None:
                    return
                self.__validatePotentialExecutable( keepGoing, a )
                if not a.isInitial():
                    continue
                self.__setState( a, Action.__Executing() )
                a.__executionBegin = time.time()
            try:
                a.doExecute()
                with self.cond:
                    self.__setState( a, Action.__Success() )
            except Exception, e:
                with self.cond:
                    self.__exceptions.append( e )
                    self.__setState( a, Action.__Failure() )
            finally:
                a.__executionEnd = time.time()

    # Methods to be called within "with self.cond:" blocks
    def __waitUntilNextPotentialExecutable( self ):
        a = self.__getNextPotentialExecutable()
        while a is None:
            if self.isEnded():
                return None
            self.cond.wait()
            a = self.__getNextPotentialExecutable()
        return a

    def __getNextPotentialExecutable( self ):
        return self.__getLowestPredecessorMatchingCriteria( lambda a: a.isInitial() and all( p.isEnded() for p in a.__predecessors ) )

    def __validatePotentialExecutable( self, keepGoing, a ):
        if len( self.__exceptions ) != 0 and not keepGoing:
            self.__setState( a, Action.__Canceled() )
        if any( p.isFailure() for p in a.__predecessors ):
            self.__setState( a, Action.__Failure() )

    def __setState( self, a, state ):
        a.__executionState = state
        self.cond.notifyAll()

    ######################################################################

    @staticmethod
    def areSame( a, b ):
        return Graphviz.Graph.areSame( a.getGraph(), b.getGraph() )

class NullAction( Action ):
    def __init__( self, preview = "" ):
        Action.__init__( self )
        self.__preview = preview
        
    def doExecute( self ):
        pass

    def computePreview( self ):
        return self.__preview
