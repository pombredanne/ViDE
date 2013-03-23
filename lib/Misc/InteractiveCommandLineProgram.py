import sys
import shlex

import recdoc as rd

class ICLPException( Exception ):
    pass

class UnknownCommand( ICLPException ):
    def __init__( self, command ):
        ICLPException.__init__( self, "Unknown command '" + command + "'" )

class UnknownOption( ICLPException ):
    def __init__( self, option ):
        ICLPException.__init__( self, "Unknown option '" + option + "'" )

class MissingOptionArgument( ICLPException ):
    def __init__( self, option ):
        ICLPException.__init__( self, "Missing arguments for option '" + option + "'" )

class TooMuchOptionArguments( ICLPException ):
    def __init__( self, option ):
        ICLPException.__init__( self, "Too much arguments for option '" + option + "'" )

class ImpossibleToDisableOption( ICLPException ):
    def __init__( self, option ):
        ICLPException.__init__( self, "Impossible to disable option '" + option + "'" )

class StoreConstant:
    def __init__( self, value ):
        self.__value = value
        self.arguments = []

    def __call__( self, destinationObject, destinationAttribute ):
        setattr( destinationObject, destinationAttribute, self.__value )

class StoreArgument:
    def __init__( self, argument ):
        self.arguments = [ argument ]

    def __call__( self, destinationObject, destinationAttribute, value ):
        if hasattr( destinationObject, destinationAttribute ):
            value = getattr( destinationObject, destinationAttribute ).__class__( value )
        setattr( destinationObject, destinationAttribute, value )

class AppendArgument:
    def __init__( self, argument ):
        self.arguments = [ argument ]

    def __call__( self, destinationObject, destinationAttribute, value ):
        getattr( destinationObject, destinationAttribute ).append( value )

class RemoveArgument:
    def __init__( self, argument ):
        self.arguments = [ argument ]

    def __call__( self, destinationObject, destinationAttribute, value ):
        getattr( destinationObject, destinationAttribute ).remove( value )

class CallWithConstant:
    def __init__( self, value ):
        self.__value = value
        self.arguments = []

    def __call__( self, destinationObject, destinationAttribute ):
        toBeCalled = getattr( destinationObject, destinationAttribute )
        toBeCalled( self.__value )

class Option:
    def __init__( self, name, aliases, destinationObject, destinationAttribute, enable, enableHelp, disable, disableHelp ):
        self.name = name
        self.__aliases = aliases
        self.__destinationObject = destinationObject
        self.__destinationAttribute = destinationAttribute
        self.__enable = enable
        self.__disable = disable
        self.enableHelp = enableHelp
        self.disableHelp = disableHelp

    def allNames( self ):
        return [ self.name ] + self.__aliases

    def argumentsForEnable( self ):
        return self.__enable.arguments

    def enable( self, *args ):
        self.__enable( self.__destinationObject, self.__destinationAttribute, *args )

    def argumentsForDisable( self ):
        if self.__disable is None:
            raise ImpossibleToDisableOption( self.name )
        return self.__disable.arguments

    def disable( self, *args ):
        if self.__disable is None:
            raise ImpossibleToDisableOption( self.name )
        self.__disable( self.__destinationObject, self.__destinationAttribute, *args )

    def canBeDisabled( self ):
        return self.__disable is not None

class OptionContainer:
    def __init__( self ):
        self.__options = dict()
        self.__groups = []
        self.__aliases = dict()

    def addOption( self, name, attribute, enable, enableHelp, disable = None, disableHelp = None ):
        if isinstance( name, str ):
            aliases = []
        else:
            names = list( name )
            name = names[ 0 ]
            aliases = names[ 1: ]
        self.__options[ name ] = Option( name, aliases, self.getAncestor(), attribute, enable, enableHelp, disable, disableHelp )
        for alias in aliases:
            self.__aliases[ alias ] = name

    def createOptionGroup( self, name, help ):
        group = OptionGroup( self, name, help )
        self.__groups.append( group )
        return group

    def processOptions( self, args ):
        cont, args = self.__enableNextOption( args )
        while cont:
            cont, args = self.__enableNextOption( args )
        return args

    def enableOption( self, optionName, args ):
        return self.__enableOption( self.__findOption( optionName ), args )

    def disableOption( self, optionName, args ):
        return self.__disableOption( self.__findOption( optionName ), args )

    def allOptions( self ):
        return ( self.__options[ o ] for o in sorted( self.__options ) )

    def allOptionGroups( self ):
        return sorted( self.__groups, key = lambda g: g.name )

    def hasOptions( self ):
        return len( self.__options ) != 0 or len( self.__groups )

    def getAncestor( self ):
        return self

    def __findOption( self, optionName ):
        ### @todo Something to force "--" with long options and "-" with short ones
        for group in self.__groups:
            try:
                return group.__findOption( optionName )
            except UnknownOption:
                pass
        if optionName in self.__aliases:
            optionName = self.__aliases[ optionName ]
        try:
            return self.__options[ optionName ]
        except KeyError:
            raise UnknownOption( optionName )

    def __enableNextOption( self, args ):
        option = self.__findNextOption( args )
        if option is None:
            return False, args
        return True, self.__enableOption( option, args[ 1: ] )

    def __findNextOption( self, args ):
        if len( args ) == 0 or not args[ 0 ].startswith( "-" ):
            return None
        return self.__findOption( args[ 0 ].lstrip( "-" ) )

    def __enableOption( self, option, args ):
        nArguments = len( option.argumentsForEnable() )
        if len( args ) < nArguments:
            raise MissingOptionArgument( option.name )
        option.enable( *args[ :nArguments ] )
        return args[ nArguments: ]

    def __disableOption( self, option, args ):
        nArguments = len( option.argumentsForDisable() )
        if len( args ) < nArguments:
            raise MissingOptionArgument( option.name )
        option.disable( *args[ :nArguments ] )
        return args[ nArguments: ]

class OptionGroup( OptionContainer ):
    def __init__( self, father, name, help ):
        OptionContainer.__init__( self )
        self.name = name
        self.help = help
        self.__father = father

    def getAncestor( self ):
        return self.__father.getAncestor()

class Command( OptionContainer ):
    def __init__( self, program ):
        OptionContainer.__init__( self )
        self.program = program

class CommandDescription:
    def __init__( self, name, commandClass, help ):
        self.name = name
        self.__commandClass = commandClass
        self.help = help

    def instance( self, program ):
        return self.__commandClass( program )

    def execute( self, program, args ):
        command = self.instance( program )
        args = command.processOptions( args )
        command.execute( args )

class CommandContainer:
    def __init__( self ):
        self.__interactiveCommands = dict()
        self.__commandLineCommands = dict()
        self.__groups = []

    def addCommand( self, name, commandClass, help ):
        command = CommandDescription( name, commandClass, help )
        self.__commandLineCommands[ name ] = command
        self.__interactiveCommands[ name ] = command

    def createCommandGroup( self, name, help ):
        group = CommandGroup( name, help )
        self.__groups.append( group )
        return group

    def addCommandLineCommand( self, name, commandClass, help ):
        command = CommandDescription( name, commandClass, help )
        self.__commandLineCommands[ name ] = command

    def addInteractiveCommand( self, name, commandClass, help ):
        command = CommandDescription( name, commandClass, help )
        self.__interactiveCommands[ name ] = command

    def allCommandGroups( self ):
        return sorted( self.__groups, key = lambda g: g.name )

    def processCommandLineCommand( self, args ):
        self.findCommandLineCommand( args[ 0 ] ).execute( self, args[ 1: ] )

    def findCommandLineCommand( self, commandName ):
        for group in self.__groups:
            try:
                return group.findCommandLineCommand( commandName )
            except UnknownCommand:
                pass
        try:
            return self.__commandLineCommands[ commandName ]
        except KeyError:
            raise UnknownCommand( commandName )

    def allCommandLineCommands( self ):
        return ( self.__commandLineCommands[ c ] for c in sorted( self.__commandLineCommands ) )

    def processInteractiveCommand( self, args ):
        self.findInteractiveCommand( args[ 0 ] ).execute( self, args[ 1: ] )

    def findInteractiveCommand( self, commandName ):
        for group in self.__groups:
            try:
                return group.findInteractiveCommand( commandName )
            except UnknownCommand:
                pass
        try:
            ### @todo unambiguous completion
            return self.__interactiveCommands[ commandName ]
        except KeyError:
            raise UnknownCommand( commandName )

    def allInteractiveCommands( self ):
        return ( self.__interactiveCommands[ c ] for c in sorted( self.__interactiveCommands ) )

class CommandGroup( CommandContainer ):
    def __init__( self, name, help ):
        CommandContainer.__init__( self )
        self.name = name
        self.help = help

class InteractiveCommandLineProgram( OptionContainer, CommandContainer ):
    ###################################################################### construction
    def __init__( self, input = sys.stdin, output = sys.stdout ):
        OptionContainer.__init__( self )
        CommandContainer.__init__( self )
        self.input = input
        self.output = output
        self.interactive = False
        self.prompt = ">"

    def addHelpCommand( self ):
        self.addCommandLineCommand( "help", InteractiveCommandLineProgram.CommandLineHelpCommand, "display this help message or help about a command (%PROG% help command-name)" )
        self.addInteractiveCommand( "help", InteractiveCommandLineProgram.InteractiveHelpCommand, "display this help message or help about a command (%PROMPT%help command-name)" )

    def addExitCommand( self ):
        self.addInteractiveCommand( "exit", InteractiveCommandLineProgram.ExitCommand, "exit the interactive command interpreter" )

    ###################################################################### execution
    def execute( self, args = sys.argv ):
        self.programName = args[ 0 ]
        args = self.processOptions( args[ 1: ] )
        if len( args ) == 0:
            self.__startInteractiveShell()
        else:
            self.processCommandLineCommand( args )

    ###################################################################### interactive shell
    class ExitCommand( Command ):
        def execute( self, args ):
            raise StopIteration()

    def __startInteractiveShell( self ):
        self.interactive = True
        try:
            while True:
                self.__processLine( self.__readNextLine() )
        except StopIteration:
            pass

    def __readNextLine( self ):
        self.output.write( self.prompt )
        self.output.flush()
        line = self.input.readline()
        if len( line ) != 0:
            return line.rstrip()
        else:
            raise StopIteration()

    def __processLine( self, line ):
        words = shlex.split( line )
        if len( words ) != 0:
            try:
                if words[ 0 ][ 0 ] == '+':
                    self.__processOption( self.enableOption, words )
                elif words[ 0 ][ 0 ] == '-':
                    self.__processOption( self.disableOption, words )
                else:
                    self.processInteractiveCommand( words )
            except ICLPException, e:
                self.output.write( str( e ) + "\n" )
                self.output.flush()

    def __processOption( self, f, words ):
        optionName = words[ 0 ][ 1: ]
        words = f( optionName, words[ 1: ] )
        if len( words ) != 0:
            raise TooMuchOptionArguments( optionName )

    ###################################################################### help
    class HelpCommand( Command ):
        def execute( self, args ):
            if len( args ) == 0:
                self.program.output.write( self.getGlobalHelp().format() )
            else:
                self.program.output.write( self.getHelpForCommand( args[ 0 ] ).format() )
            self.program.output.flush()

        def getGlobalHelp( self ):
            help = rd.Document()
            section = self.getHelpSectionForUsage()
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForOptions()
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForCommands()
            if section is not None:
                help.add( section )
            return help

        def replaceStrings( self, text ):
            return text.replace( "%PROG%", self.program.programName ).replace( "%PROMPT%", self.program.prompt )

        def getHelpSectionForCommands( self ):
            return self.__getHelpSectionForCommands( self.program, "Commands" )
        
        def __getHelpSectionForCommands( self, container, title ):
            section = rd.Section( title )
            list = rd.DefinitionList()
            section.add( list )
            for c in self.allCommands( container ):
                if c.help is not None:
                    list.add( c.name, self.replaceStrings( c.help ) )
            for g in container.allCommandGroups():
                subSection = self.__getHelpSectionForCommands( g, g.name )
                if subSection is not None:
                    section.add( subSection )
            return section

        def getHelpSectionForCommandSummary( self, command ):
            section = rd.Section( "Summary" )
            section.add( rd.Paragraph( command.help ) )
            return section

        def getHelpSectionForDashedOptions( self, container, title = "Options" ):
            if not container.hasOptions():
                return None
            section = rd.Section( title )
            list = rd.DefinitionList()
            section.add( list )
            for o in container.allOptions():
                list.add( ", ".join( " ".join( [ ( "--" if len( name ) > 1 else "-" ) + name ] + o.argumentsForEnable() ) for name in o.allNames() ), self.replaceStrings( o.enableHelp ) )
            for g in container.allOptionGroups():
                subSection = self.getHelpSectionForDashedOptions( g, g.name )
                if subSection is not None:
                    section.add( subSection )
            return section

        def getHelpSectionForCommandOptions( self, command ):
            command = command.instance( self )
            return self.getHelpSectionForDashedOptions( command )

    class CommandLineHelpCommand( HelpCommand ):
        def getHelpSectionForUsage( self ):
            section = rd.Section( "Usage" )
            section.add( rd.Paragraph( self.replaceStrings( "%PROG% [options] [command [...]]" ) ) )
            return section

        def getHelpSectionForOptions( self ):
            return self.getHelpSectionForDashedOptions( self.program )

        def allCommands( self, container ):
            return container.allCommandLineCommands()

        def getHelpForCommand( self, commandName ):
            command = self.program.findCommandLineCommand( commandName )
            help = rd.Document()
            section = self.getHelpSectionForCommandUsage( command )
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForOptions()
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForCommandSummary( command )
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForCommandOptions( command )
            if section is not None:
                help.add( section )
            return help

        def getHelpSectionForCommandUsage( self, command ):
            section = rd.Section( "Usage" )
            section.add( rd.Paragraph( self.replaceStrings( "%PROG% [options] " + command.name + " [options]" ) ) )
            return section

    class InteractiveHelpCommand( HelpCommand ):
        def getHelpSectionForUsage( self ):
            return None

        def getHelpSectionForOptions( self ):
            return self.getHelpSectionForPlusMinusOptions( self.program )

        def getHelpSectionForPlusMinusOptions( self, container, title = "Options" ):
            section = rd.Section( title )
            list = rd.DefinitionList()
            section.add( list )
            for o in container.allOptions():
                list.add( ", ".join( " ".join( [ "+" + name ] + o.argumentsForEnable() ) for name in o.allNames() ), self.replaceStrings( o.enableHelp ) )
                if o.canBeDisabled():
                    list.add( ", ".join( " ".join( [ "-" + name ] + o.argumentsForDisable() ) for name in o.allNames() ), self.replaceStrings( o.disableHelp ) )
            for g in container.allOptionGroups():
                subSection = self.getHelpSectionForPlusMinusOptions( g, g.name )
                if subSection is not None:
                    section.add( subSection )
            return section

        def allCommands( self, container ):
            return container.allInteractiveCommands()

        def getHelpForCommand( self, commandName ):
            command = self.program.findInteractiveCommand( commandName )
            help = rd.Document()
            section = self.getHelpSectionForCommandUsage( command )
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForCommandSummary( command )
            if section is not None:
                help.add( section )
            section = self.getHelpSectionForCommandOptions( command )
            if section is not None:
                help.add( section )
            return help

        def getHelpSectionForCommandUsage( self, command ):
            section = rd.Section( "Usage" )
            section.add( rd.Paragraph( command.name + " [options]" ) )
            return section

if __name__ == "__main__":
    class TestProgram( InteractiveCommandLineProgram ):
        def __init__( self ):
            InteractiveCommandLineProgram.__init__( self )

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

            longCommands = self.createCommandGroup( "Long commands", "Blih blih blih blih blih blih blih blih blih blih blih blih blih blih" )
            longCommands.addCommand( "long-command", TestProgram.LongCommand, "process long command with a long help message blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah" )

            self.addHelpCommand()
            
            self.addExitCommand()

        class ShortCommand( Command ):
            def execute( self, args ):
                self.program.executionMock.doShortCommand( args )

        class LongCommand( Command ):
            def __init__( self, program ):
                Command.__init__( self, program )

                self.aaa = "aaa"
                self.addOption( "aaa", "aaa", StoreArgument( "AAA" ), "set aaa to AAA" )

            def execute( self, args ):
                self.program.executionMock.doLongCommand( self.aaa, args )

    TestProgram().execute( sys.argv )
