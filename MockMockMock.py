import unittest

class MockException( Exception ): pass
class UnexpectedCall( MockException ): pass
class ExpectedMoreCalls( MockException ):
    def __init__( self ):
        MockException.__init__( self, "Expected more calls" )

class MockFunction:
    def __init__( self, mockMaker, mock, name ):
        self.__mockMaker = mockMaker
        self.__mock = mock
        self.__name = name

    def __call__( self, *args ):
        return self.__mockMaker.processMockFunctionCall( self.__mock, self.__name, *args )

class Group:
    def __init__( self, mockMaker ):
        self.__mockMaker = mockMaker
        self.expectedCalls = list()

    def __enter__( self ):
        self.__mockMaker.pushGroup( self )

    def __exit__( self, exc_type, exc_value, traceback ):
        self.__mockMaker.popGroup()

    def add( self, c  ):
        self.expectedCalls.append( c )

    def isEmpty( self ):
        return len( self.expectedCalls ) == 0

    def mustBeRemoved( self ):
        return self.isEmpty()

    def canBeSkipped( self ):
        return all( c.canBeSkipped() for c in self.expectedCalls )

class OrderedGroup( Group ):
    def execute( self, mock, name, *args ):
        for i, c in enumerate( self.expectedCalls ):
            if not c.canBeSkipped() or c.canExecute( mock, name, *args ):
                self.expectedCalls = self.expectedCalls[i:]
                try:
                    return c.execute( mock, name, *args )
                finally:
                    if c.mustBeRemoved():
                        self.expectedCalls = self.expectedCalls[1:]
        raise UnexpectedCall( "Unexpected call to " + mock._Mock__name + "." + name + str( args ) )

    def canExecute( self, mock, name, *args ):
        for c in self.expectedCalls:
            if c.canExecute( mock, name, *args ):
                return True
            if not c.canBeSkipped():
                return False;
        return False

class UnorderedGroup( Group ):
    def execute( self, mock, name, *args ):
        for i, c in enumerate( self.expectedCalls ):
            if c.canExecute(  mock, name, *args ):
                try:
                    return c.execute( mock, name, *args )
                finally:
                    if c.mustBeRemoved():
                        self.expectedCalls = self.expectedCalls[:i] + self.expectedCalls[i+1:]
        raise UnexpectedCall( "Unexpected call to " + mock._Mock__name + "." + name + str( args ) )

    def canExecute( self, mock, name, *args ):
        return any( c.canExecute(  mock, name, *args ) for c in self.expectedCalls )

# @todo Maybe replace FunctionCall.isOptional by a class OptionalGroup( Group )
# @todo Maybe replace mustBeRemoved (and maybe canBeSkipped) by a simplify method

# @todo Create a FunctionCallDescription for returns, raises, lasts, etc. Keep FunctionCall for other methods
class FunctionCall:
    def __init__( self, mock, name, *args ):
        self.__mock = mock
        self.__name = name
        self.__args = args
        self.__returnValue = None
        self.__exception = None
        self.__optional = False

    def returns( self, returnValue ):
        self.__returnValue = returnValue
        return self

    def raises( self, exception ):
        self.__exception = exception
        return self

    def isOptional( self ):
        self.__optional = True
        return self

    def execute( self, mock, name, *args ):
        self.checkCall( mock, name, *args )
        if self.__exception is not None:
            raise self.__exception
        return self.__returnValue

    def checkCall( self, mock, name, *args ):
        if not self.canExecute( mock, name, *args ):
            raise UnexpectedCall( "Unexpected call to " + mock._Mock__name + "." + name + str( args ) + " instead of " + self.__mock._Mock__name + "." + self.__name + str( self.__args ) )

    def canExecute( self, mock, name, *args ):
        return mock == self.__mock and name == self.__name and args == self.__args

    def canBeSkipped( self ):
        return self.__optional

    def mustBeRemoved( self ):
        return True

class MockMaker:
    def __init__( self ):
        self.__recording = True
        self.__expectedCalls = OrderedGroup( self )
        self.__groups = [ self.__expectedCalls ]
        self.__testWasOk = True

    def createMock( self, name, classToMock = None, *args ):
        class Nothing:
            pass
        if classToMock is None:
            classToMock = Nothing
        class Mock( classToMock ):
            def __init__( self, mockMaker, name, *args ):
                if hasattr( classToMock, "__init__" ):
                    classToMock.__init__( self, *args )
                self.__mockMaker = mockMaker
                self.__mockedFunctions = set()
                self.__name = name

            def __getattr__( self, name ):
                if name.startswith( "__" ) and name not in [ "__call__" ]:
                    return classToMock.__getattr__( self, name )
                try:
                    return self.__mockMaker.addMockFunction( self, name )
                except MockException:
                    if hasattr( classToMock, "__getattr__" ):
                        return classToMock.__getattr__( self, name )
                    raise

        return Mock( self, name, *args )

    def startTest( self ):
        assert( len( self.__groups ) == 1 )
        self.__recording = False

    def endTest( self ):
        if not self.__expectedCalls.isEmpty() and not self.__expectedCalls.canBeSkipped() and self.__testWasOk:
            self.__testWasOk = False
            raise ExpectedMoreCalls()

    def addMockFunction( self, mock, name ):
        if not self.__recording:
            raise UnexpectedCall( "Unexpected call to " + mock._Mock__name + "." + name )
        f = MockFunction( self, mock, name )
        setattr( mock, name, f )
        return f

    def processMockFunctionCall( self, mock, name, *args ):
        if self.__recording:
            return self.recordFunctionCall( mock, name, *args )
        else:
            return self.replayFunctionCall( mock, name, *args )

    def recordFunctionCall( self, mock, name, *args ):
        c = FunctionCall( mock, name, *args )
        self.__groups[-1].add( c )
        return c

    def replayFunctionCall( self, mock, name, *args ):
        try:
            return self.__expectedCalls.execute( mock, name, *args )
        except MockException:
            self.__testWasOk = False
            raise

    def pushGroup( self, g ):
        self.__groups[-1].add( g )
        self.__groups.append( g )

    def popGroup( self ):
        self.__groups = self.__groups[:-1]

    def orderedGroup( self ):
        return OrderedGroup( self )

    def unorderedGroup( self ):
        return UnorderedGroup( self )

class TestCase( unittest.TestCase ):
    def setUp( self ):
        self.m = MockMaker()

    def tearDown( self ):
        self.m.endTest()
