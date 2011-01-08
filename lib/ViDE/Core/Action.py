from __future__ import with_statement

import threading
import itertools
import time

class CompoundException( Exception ):
    def __init__( self, exceptions ):
        self.__exceptions = exceptions

    def __str__( self ):
        return "CompoundException( " + str( self.__exceptions ) + " )"

class Action:
    ###################################################################### construction

    def __init__( self ):
        self.__predecessors = set()

    def addPredecessor( self, p ):
        self.__predecessors.add( p )

    def getPredecessors( self ):
        return self.__predecessors
        
    ###################################################################### height-based accessors

    def __getLowestPredecessorMatchingCriteria( self, criteria ):
        next = self
        for p in self.__predecessors:
            n = p.__getLowestPredecessorMatchingCriteria( criteria )
            if n is not None and n.__height() < next.__height():
                next = n
        if criteria( next ):
            return next
        else:
            return None

    def __height( self ):
        if len( self.__predecessors ) == 0:
            return 0
        return max( p.__height() for p in self.__predecessors ) + 1

    ###################################################################### preview

    def preview( self ):
        self.__clearPreviewFlags()
        return self.__preview()

    def __preview( self ):
        preview = []
        while True:
            next = self.__getNextToPreview()
            if next is None:
                break
            next.__previewed = True
            text = next.doPreview()
            if text != "":
                preview.append( text )
        return preview

    def __getNextToPreview( self ):
        return self.__getLowestPredecessorMatchingCriteria( lambda a: not a.__previewed )

    def __clearPreviewFlags( self ):
        self.__previewed = False
        for p in self.__predecessors:
            p.__clearPreviewFlags()

    ###################################################################### execution state

    class __ExecutionState:
        def __getattr__( self, attr ):
            if attr.startswith( "is" ):
                return lambda: False
            raise AttributeError()
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

    def __getattr__( self, attr ):
        if attr.startswith( "is" ):
            return getattr( self.__executionState, attr )
        raise AttributeError()

    def getExecutionTimes( self ):
        return self.__executionBegin, self.__executionEnd
        
    ###################################################################### execute

    def execute( self, keepGoing, threadNumber ):
        self.__prepareExecution()
        self.__executeInThreads( keepGoing, threadNumber )
        self.__checkExecution()

    def __prepareExecution( self ):
        self.__exceptions = []
        self.cond = threading.Condition()
        self.__resetExecutionState()

    def __resetExecutionState( self ):
        self.__executionState = Action.__Initial()
        self.__executionBegin = None
        self.__executionEnd = None
        for p in self.__predecessors:
            p.__resetExecutionState()

    def __checkExecution( self ):
        del self.cond
        if len( self.__exceptions ) != 0:
            raise CompoundException( self.__exceptions )

    def __executeInThreads( self, keepGoing, threadNumber ):
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
        return Action.__haveSameStructure( a, b ) and Action.__haveSameModel( a, b )

    @staticmethod
    def __haveSameStructure( a, b, d = dict() ):
        if a in d and d[ a ] is not b:
            return False
        d[ a ] = b
        if len( a.__predecessors ) != len( b.__predecessors ):
            return False
        ### @todo Bug: nothing guaranties that matching predecessors will be in the same order in both graphs
        ### But graph matching algorithms are too complex to be implemented right now
        return all( itertools.imap( lambda ap, bp: Action.__haveSameStructure( ap, bp, d ), a.__predecessors, b.__predecessors ) )

    @staticmethod
    def __haveSameModel( a, b ):
        pA, dA = Action.__buildModel( a )
        pB, dB = Action.__buildModel( b )
        return pA == pB and dA == dB

    @staticmethod
    def __buildModel( a ):
        pA = a.doPreview()
        dA = {}
        for p in a.__predecessors:
            pp, dp = Action.__buildModel( p )
            dA[ pp ] = dp
        return pA, dA

class ActionModel( Action ):
    def __init__( self, preview ):
        Action.__init__( self )
        self.__preview = preview

    def doPreview( self ):
        return self.__preview

    @staticmethod
    def build( d ):
        return ActionModel.__build( d )[ 0 ]

    @staticmethod
    def __build( d ):
        actions = []
        for preview in d:
            a = ActionModel( preview )
            for p in ActionModel.__build( d[ preview ] ):
                a.addPredecessor( p )
            actions.append( a )
        return actions

class NullAction( Action ):
    def __init__( self ):
        Action.__init__( self )

    def doExecute( self ):
        pass

    def doPreview( self ):
        return ""