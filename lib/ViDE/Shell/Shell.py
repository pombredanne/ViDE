from Misc import InteractiveCommandLineProgram

from ViDE import Log
from ViDE.Shell.AutoTest import AutoTest
from ViDE.Shell.Make import Make
from ViDE.Shell.Draw import Draw
from ViDE.Shell.Daemon import Daemon

# Get from ViDE
defaultToolset = "Toolset1"
availableToolsets = [ "Toolset1", "Toolset2", "Toolset3" ]

defaultBuildkit = "gcc"
availableBuildkits = [ "Buildkit1", "Buildkit2", "Buildkit3" ]

class Shell( InteractiveCommandLineProgram.InteractiveCommandLineProgram ):
    def __init__( self ):
        InteractiveCommandLineProgram.InteractiveCommandLineProgram.__init__( self )
        self.prompt = "ViDE>"

        verbosity = self.createOptionGroup( "Verbosity", "" )
        verbosity.addOption( [ "q", "quiet" ], "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 0 ), "print as few messages as possible", InteractiveCommandLineProgram.CallWithConstant( 1 ), "print normal messages" )
        verbosity.addOption( [ "v", "verbose" ], "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 2 ), "print more information messages", InteractiveCommandLineProgram.CallWithConstant( 1 ), "don't print information messages" )
        verbosity.addOption( "debug", "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 3 ), "print debug messages", InteractiveCommandLineProgram.CallWithConstant( 1 ), "don't print debug messages" )

        toolsChoice = self.createOptionGroup( "Tools choice", "" )
        self.toolset = defaultToolset
        toolsChoice.addOption( "toolset", "toolset", InteractiveCommandLineProgram.StoreArgument( "TOOLSET" ), "use toolset TOOLSET", InteractiveCommandLineProgram.StoreConstant( defaultToolset ), "use default toolset" )

        self.buildkit = defaultBuildkit
        toolsChoice.addOption( "buildkit", "buildkit", InteractiveCommandLineProgram.StoreArgument( "BUILDKIT" ), "use buildkit BUILDKIT", InteractiveCommandLineProgram.StoreConstant( defaultBuildkit ), "use default buildkit" )

        generation = self.createCommandGroup( "Artifact generation", "" )
        generation.addCommand( "make", Make, "build the project" )
        
        self.addCommand( "draw", Draw, "print the dot graph of the project" )
        self.addCommand( "autotest", AutoTest, "run ViDE's own unit tests" )
        self.addCommand( "daemon", Daemon, "launch the continous integration daemon" )

        self.addHelpCommand()
        self.addExitCommand()
    
    def setVerbosity( self, verbosity ):
        Log.level = verbosity
