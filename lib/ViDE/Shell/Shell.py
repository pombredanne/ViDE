from Misc import InteractiveCommandLineProgram

from ViDE.Shell.AutoTest import AutoTest
from ViDE.Shell.Make import Make

# Get from ViDE
defaultToolset = "Toolset1"
availableToolsets = [ "Toolset1", "Toolset2", "Toolset3" ]

defaultBuildkit = "Buildkit1"
availableBuildkits = [ "Buildkit1", "Buildkit2", "Buildkit3" ]

# Implement in ViDE
def DummyCommand( name ):
    class Dummy( InteractiveCommandLineProgram.Command ):
        def execute( self, args ):
            print "called", name
    return Dummy

class Shell( InteractiveCommandLineProgram.InteractiveCommandLineProgram ):
    def __init__( self ):
        InteractiveCommandLineProgram.InteractiveCommandLineProgram.__init__( self )
        self.prompt = "ViDE>"

        self.verbosity = 1
        verbosity = self.createOptionGroup( "Verbosity", "" )
        verbosity.addOption( [ "q", "quiet" ], "verbosity", InteractiveCommandLineProgram.StoreConstant( 0 ), "print as few messages as possible", InteractiveCommandLineProgram.StoreConstant( 1 ), "print normal messages" )
        verbosity.addOption( [ "v", "verbose" ], "verbosity", InteractiveCommandLineProgram.StoreConstant( 2 ), "print information messages", InteractiveCommandLineProgram.StoreConstant( 1 ), "don't print information messages" )
        verbosity.addOption( "debug", "verbosity", InteractiveCommandLineProgram.StoreConstant( 3 ), "print debug messages", InteractiveCommandLineProgram.StoreConstant( 1 ), "don't print debug messages" )

        toolsChoice = self.createOptionGroup( "Tools choice", "" )
        self.toolset = defaultToolset
        toolsChoice.addOption( "toolset", "toolset", InteractiveCommandLineProgram.StoreArgument( "TOOLSET" ), "use toolset TOOLSET", InteractiveCommandLineProgram.StoreConstant( defaultToolset ), "use default toolset" )

        self.buildkit = defaultBuildkit
        toolsChoice.addOption( "buildkit", "buildkit", InteractiveCommandLineProgram.StoreArgument( "BUILDKIT" ), "use buildkit BUILDKIT", InteractiveCommandLineProgram.StoreConstant( defaultBuildkit ), "use default buildkit" )

        generation = self.createCommandGroup( "Artifact generation", "" )
        generation.addCommand( "make", Make, "build the project" )
        
        self.addCommand( "autotest", AutoTest, "run ViDE's own unit tests" )

        self.addHelpCommand()
        self.addExitCommand()
