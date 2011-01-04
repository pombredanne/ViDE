import unittest
import textwrap

import MockMockMock

from InteractiveCommandLineProgram import InteractiveCommandLineProgram, Command
from InteractiveCommandLineProgram import StoreArgument, StoreConstant, AppendArgument, RemoveArgument
from InteractiveCommandLineProgram import UnknownCommand, UnknownOption

class TestProgram( InteractiveCommandLineProgram ):
    def __init__( self, input, output, executionMock ):
        InteractiveCommandLineProgram.__init__( self, input, output )
        self.executionMock = executionMock

        self.stringScalar = "A"
        self.addOption( "stringB", "stringScalar", StoreConstant( "B" ), "set a string to B", StoreConstant( "A" ), "set a string to A" )
        self.addOption( "string", "stringScalar", StoreArgument( "STRING" ), "set a string to STRING" )

        self.intScalar = 1
        self.addOption( ( "int", "i", "integer", "j" ), "intScalar", StoreArgument( "INT" ), "set an int to INT" )

        self.stringList = [ "A", "B", "C" ]
        collectionManagement = self.createOptionGroup( "Collection management", "blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )
        collectionManagement.addOption( "add", "stringList", AppendArgument( "ELEMENT" ), "add an element ELEMENT", RemoveArgument( "ELEMENT" ), "remove an element ELEMENT" )
        collectionManagement.addOption( ( "remove", "r" ), "stringList", RemoveArgument( "ELEMENT" ), "remove an element ELEMENT", AppendArgument( "ELEMENT" ), "add an element ELEMENT" )

        self.addCommand( "command", TestProgram.ShortCommand, "process command" )
        self.addCommand( "commic", TestProgram.FunnyCommand, "be funny" )
        self.addCommand( "commute", TestProgram.CommuteCommand, None ) # Does not appear in help. Is not candidate to completion

        longCommands = self.createCommandGroup( "Long commands", "Blih blih blih blih blih blih blih blih blih blih blih blih blih blih" )
        longCommands.addCommand( "long-command", TestProgram.LongCommand, "process long command with a long help message blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )

        self.addHelpCommand()
        
        self.addExitCommand()

    class ShortCommand( Command ):
        def execute( self, args ):
            self.program.executionMock.doShortCommand( args )

    class CommuteCommand( Command ):
        def execute( self, args ):
            self.program.executionMock.doCommuteCommand( args )

    class FunnyCommand( Command ):
        def execute( self, args ):
            self.program.executionMock.doFunnyCommand( args )

    class LongCommand( Command ):
        def __init__( self, program ):
            Command.__init__( self, program )

            self.aaa = "aaa"
            self.addOption( "aaa", "aaa", StoreArgument( "AAA" ), "set aaa to AAA" )

        def execute( self, args ):
            self.program.executionMock.doLongCommand( self.aaa, args )

class TestCase( MockMockMock.TestCase ):
    def setUp( self ):
        MockMockMock.TestCase.setUp( self )
        self.input = self.m.createMock( "self.input" )
        self.output = self.m.createMock( "self.output" )
        self.executionMock = self.m.createMock( "self.executionMock" )

        self.p = TestProgram( self.input, self.output, self.executionMock )

    def readline( self, line ):
        self.output.write( ">" )
        self.output.flush()
        self.input.readline().returns( line )

class CommandLine( TestCase ):
    def testSimplestUse( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "command" ] )
        self.assertEquals( self.p.stringScalar, "A" )
        self.assertEquals( self.p.intScalar, 1 )

    def testUnknownCommand( self ):
        self.m.startTest()
        self.assertRaises( UnknownCommand, self.p.execute, [ "test", "unknown" ] )

    def testUnknownOption( self ):
        self.m.startTest()
        self.assertRaises( UnknownOption, self.p.execute, [ "test", "--unknown", "command" ] )

    def testArgumentsForwarding( self ):
        self.executionMock.doShortCommand( [ "arg1", "arg2" ] )
        self.m.startTest()
        self.p.execute( [ "test", "command", "arg1", "arg2" ] )
        self.assertEquals( self.p.stringScalar, "A" )

    def testStoreConstantGlobalOption( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--stringB", "command" ] )
        self.assertEquals( self.p.stringScalar, "B" )

    def testStoreArgumentStringGlobalOption( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--string", "C", "command" ] )
        self.assertEquals( self.p.stringScalar, "C" )

    def testStoreArgumentIntGlobalOption( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--int", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 ) # Type is important: intScalar is still an int

    def testGlobalOptionAlias_1( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--integer", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )

    def testGlobalOptionAlias_2( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "-i", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )

    def testGlobalOptionAlias_3( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "-j", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )

    # def testShortAndLongOptionForms( self ):
        # self.m.startTest()
        # self.assertRaises( UnknownOption, self.p.execute, [ "test", "--i", "42", "command" ] )
        # self.assertRaises( UnknownOption, self.p.execute, [ "test", "-int", "42", "command" ] )

    def testAppendArgumentGlobalOption( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--add", "D", "command" ] )
        self.assertEquals( self.p.stringList, [ "A", "B", "C", "D" ] )

    def testRemoveArgumentGlobalOption( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--remove", "B", "command" ] )
        self.assertEquals( self.p.stringList, [ "A", "C" ] )

    def testSeveralGlobalOptions_1( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--int", "42", "--stringB", "--add", "D", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )
        self.assertEquals( self.p.stringScalar, "B" )
        self.assertEquals( self.p.stringList, [ "A", "B", "C", "D" ] )

    def testSeveralGlobalOptions_2( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--stringB", "--remove", "B", "--int", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )
        self.assertEquals( self.p.stringScalar, "B" )
        self.assertEquals( self.p.stringList, [ "A", "C" ] )

    def testSeveralGlobalOptions_3( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--string", "C", "--add", "D", "--int", "42", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )
        self.assertEquals( self.p.stringScalar, "C" )
        self.assertEquals( self.p.stringList, [ "A", "B", "C", "D" ] )

    def testSeveralGlobalOptions_4( self ):
        self.executionMock.doShortCommand( [] )
        self.m.startTest()
        self.p.execute( [ "test", "--remove", "B", "--int", "42", "--string", "C", "command" ] )
        self.assertEquals( self.p.intScalar, 42 )
        self.assertEquals( self.p.stringScalar, "C" )
        self.assertEquals( self.p.stringList, [ "A", "C" ] )

    def testCommandDefaultOption( self ):
        self.executionMock.doLongCommand( "aaa", [] )
        self.m.startTest()
        self.p.execute( [ "test", "long-command" ] )

    def testCommandOption( self ):
        self.executionMock.doLongCommand( "xxx", [] )
        self.m.startTest()
        self.p.execute( [ "test", "long-command", "--aaa", "xxx" ] )
        
    def testNoCommandCompletion( self ):
        self.m.startTest()
        self.assertRaises( UnknownCommand, self.p.execute, [ "test", "commut" ] )

class InteractiveShellCommands( TestCase ):
    def testSimplestUse( self ):
        self.readline( "command" )
        self.executionMock.doShortCommand( [] )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testArgumentsForwarding( self ):
        self.readline( "command arg1 arg2" )
        self.executionMock.doShortCommand( [ "arg1", "arg2" ] )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testQuotedArgumentsForwarding( self ):
        self.readline( "command \"arg1 arg2\"" )
        self.executionMock.doShortCommand( [ "arg1 arg2" ] )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testCommandDefaultOption( self ):
        self.readline( "long-command" )
        self.executionMock.doLongCommand( "aaa", [] )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testCommandOption( self ):
        self.readline( "long-command --aaa xxx" )
        self.executionMock.doLongCommand( "xxx", [] )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testUnknownCommand( self ):
        self.readline( "unknown" )
        self.output.write( "Unknown command 'unknown'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testTerminationWithEof( self ):
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testTerminationWithExit( self ):
        self.readline( "exit" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testAmbiguousCommandCompletion( self ):
        self.readline( "comm" )
        self.output.write( "Unknown command 'comm'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testCommandCompletion( self ):
        self.readline( "commi" )
        self.executionMock.doFunnytCommand()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testNoCommandCompletion( self ):
        self.readline( "commu" )
        self.output.write( "Unknown command 'commu'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

class InteractiveShellOptionEnable( TestCase ):
    def testEnableOptionWithoutArgument( self ):
        self.readline( "+stringB" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )
        self.assertEquals( self.p.stringScalar, "B" )

    def testEnableOptionWithArgument( self ):
        self.readline( "+string C" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )
        self.assertEquals( self.p.stringScalar, "C" )

    def testEnableOptionAlias( self ):
        self.readline( "+integer 42" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )
        self.assertEquals( self.p.intScalar, 42 )

    def testEnableOptionWithQuotedArgument( self ):
        self.readline( "+string \"C C\"" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )
        self.assertEquals( self.p.stringScalar, "C C" )

    def testEnableOptionWithTooMuchArguments( self ):
        self.readline( "+string C D E" )
        self.output.write( "Too much arguments for option 'string'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testEnableOptionMissingArgument( self ):
        self.readline( "+string" )
        self.output.write( "Missing arguments for option 'string'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testEnableUnknownOption( self ):
        self.readline( "+unknown" )
        self.output.write( "Unknown option 'unknown'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

class InteractiveShellOptionDisable( TestCase ):
    def testDisableOptionWithoutArgument( self ):
        self.readline( "-stringB" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test", "--string", "C" ] )
        self.assertEquals( self.p.stringScalar, "A" )

    def testDisableOptionWithArguments( self ):
        self.readline( "-add B" )
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )
        self.assertEquals( self.p.stringList, [ "A", "C" ] )

    def testDisableOptionWithTooMuchArguments( self ):
        self.readline( "-stringB C D E" )
        self.output.write( "Too much arguments for option 'stringB'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testDisableOptionMissingArgument( self ):
        self.readline( "-add" )
        self.output.write( "Missing arguments for option 'add'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testDisableOptionWithNoDisableAction( self ):
        self.readline( "-int" )
        self.output.write( "Impossible to disable option 'int'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testDisableUnknownOption( self ):
        self.readline( "-unknown" )
        self.output.write( "Unknown option 'unknown'\n" )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

class Help( TestCase ):
    # def testCommandLineHelpOption( self ):
        # self.m.startTest()
        # self.p.execute( [ "test", "--help" ] )

    def testCommandLineHelpCommand( self ):
        self.output.write( textwrap.dedent( """\
            Usage:
              test [options] [command [...]]
            
            Options:
              --int INT, -i INT, --integer INT, -j INT
                               set an int to INT
              --string STRING  set a string to STRING
              --stringB        set a string to B
            
              Collection management:
                --add ELEMENT  add an element ELEMENT
                --remove ELEMENT, -r ELEMENT
                               remove an element ELEMENT
            
            Commands:
              command  process command
              commic   be funny
              help     display this help message or help about a command (test
                       help command-name)
            
              Long commands:
                long-command  process long command with a long help message blah
                              blah blah blah blah blah blah blah blah blah blah
                              blah blah blah blah blah blah blah
            """ ) )
        self.output.flush()
        self.m.startTest()
        self.p.execute( [ "test", "help" ] )

    def testCommandLineHelpCommandWithArgument( self ):
        self.output.write( textwrap.dedent( """\
            Usage:
              test [options] command [options]
            
            Options:
              --int INT, -i INT, --integer INT, -j INT
                               set an int to INT
              --string STRING  set a string to STRING
              --stringB        set a string to B
            
              Collection management:
                --add ELEMENT  add an element ELEMENT
                --remove ELEMENT, -r ELEMENT
                               remove an element ELEMENT
            
            Summary:
              process command
            """ ) )
        self.output.flush()
        self.output.write( textwrap.dedent( """\
            Usage:
              test [options] long-command [options]
            
            Options:
              --int INT, -i INT, --integer INT, -j INT
                               set an int to INT
              --string STRING  set a string to STRING
              --stringB        set a string to B
            
              Collection management:
                --add ELEMENT  add an element ELEMENT
                --remove ELEMENT, -r ELEMENT
                               remove an element ELEMENT
            
            Summary:
              process long command with a long help message blah blah blah blah
              blah blah blah blah blah blah blah blah blah blah blah blah blah
              blah
            
            Options:
              --aaa AAA  set aaa to AAA
            """ ) )
        self.output.flush()
        self.m.startTest()
        self.p.execute( [ "test", "help", "command" ] )
        self.p.execute( [ "test", "help", "long-command" ] )

    def testInteractiveHelpCommand( self ):
        self.readline( "help" )
        self.output.write( textwrap.dedent( """\
            Options:
              +int INT, +i INT, +integer INT, +j INT
                              set an int to INT
              +string STRING  set a string to STRING
              +stringB        set a string to B
              -stringB        set a string to A
            
              Collection management:
                +add ELEMENT  add an element ELEMENT
                -add ELEMENT  remove an element ELEMENT
                +remove ELEMENT, +r ELEMENT
                              remove an element ELEMENT
                -remove ELEMENT, -r ELEMENT
                              add an element ELEMENT
            
            Commands:
              command  process command
              commic   be funny
              exit     exit the interactive command interpreter
              help     display this help message or help about a command (>help
                       command-name)
            
              Long commands:
                long-command  process long command with a long help message blah
                              blah blah blah blah blah blah blah blah blah blah
                              blah blah blah blah blah blah blah
            """ ) )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

    def testInteractiveHelpCommandWithArgument( self ):
        self.readline( "help command" )
        self.output.write( textwrap.dedent( """\
            Usage:
              command [options]
            
            Summary:
              process command
            """ ) )
        self.output.flush()
        self.readline( "help long-command" )
        self.output.write( textwrap.dedent( """\
            Usage:
              long-command [options]
            
            Summary:
              process long command with a long help message blah blah blah blah
              blah blah blah blah blah blah blah blah blah blah blah blah blah
              blah
            
            Options:
              --aaa AAA  set aaa to AAA
            """ ) )
        self.output.flush()
        self.readline( "" )
        self.m.startTest()
        self.p.execute( [ "test" ] )

unittest.main()
