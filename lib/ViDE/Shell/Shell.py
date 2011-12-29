from Misc import InteractiveCommandLineProgram

from ViDE import Log
from ViDE.Shell.AutoTest import AutoTest
from ViDE.Shell.Make import Make
from ViDE.Shell.Run import Run
from ViDE.Shell.Debug import Debug
from ViDE.Shell.InstallTools import InstallTools
from ViDE.Shell.CheckImports import CheckImports

class Shell( InteractiveCommandLineProgram.InteractiveCommandLineProgram ):
    def __init__( self ):
        InteractiveCommandLineProgram.InteractiveCommandLineProgram.__init__( self )
        self.prompt = "ViDE>"

        verbosity = self.createOptionGroup( "Verbosity", "" )
        verbosity.addOption( "silent", "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( -1 ), "print absolutely nothing (not even error messages)", InteractiveCommandLineProgram.CallWithConstant( 1 ), "print normal messages" )
        verbosity.addOption( [ "q", "quiet" ], "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 0 ), "print as few messages as possible", InteractiveCommandLineProgram.CallWithConstant( 1 ), "print normal messages" )
        verbosity.addOption( [ "v", "verbose" ], "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 2 ), "print more information messages", InteractiveCommandLineProgram.CallWithConstant( 1 ), "don't print information messages" )
        verbosity.addOption( "debug", "setVerbosity", InteractiveCommandLineProgram.CallWithConstant( 3 ), "print debug messages", InteractiveCommandLineProgram.CallWithConstant( 1 ), "don't print debug messages" )

        toolsChoice = self.createOptionGroup( "Tools choice", "" )

        self.hostPlatform = ""

        self.targetPlatform = ""
        toolsChoice.addOption( [ "t", "target-platform" ], "targetPlatform", InteractiveCommandLineProgram.StoreArgument( "TARGET-PLATFORM" ), "target platform TARGET-PLATFORM", InteractiveCommandLineProgram.StoreConstant( "" ), "target current platform" )

        self.toolset = ""
        # toolsChoice.addOption( [ "t", "toolset" ], "toolset", InteractiveCommandLineProgram.StoreArgument( "TOOLSET" ), "use toolset TOOLSET", InteractiveCommandLineProgram.StoreConstant( "" ), "use default toolset" )

        self.buildkit = ""
        toolsChoice.addOption( [ "b", "buildkit" ], "buildkit", InteractiveCommandLineProgram.StoreArgument( "BUILDKIT" ), "use buildkit BUILDKIT", InteractiveCommandLineProgram.StoreConstant( "" ), "use default buildkit" )

        self.flavour = ""
        toolsChoice.addOption( [ "f", "flavour" ], "flavour", InteractiveCommandLineProgram.StoreArgument( "FLAVOUR" ), "use flavour FLAVOUR", InteractiveCommandLineProgram.StoreConstant( "" ), "use default flavour" )

        generation = self.createCommandGroup( "Artifact generation", "" )
        generation.addCommand( "make", Make, "build the project" )
        
        self.addCommand( "run", Run, "run an executable file" )
        self.addCommand( "debug", Debug, "debug an executable file" )
        self.addCommand( "install-tools", InstallTools, "install tools" )

        autodiagnostic = self.createCommandGroup( "ViDE's auto diagnostic", "" )
        autodiagnostic.addCommand( "autotest", AutoTest, "run ViDE's own unit tests" )
        autodiagnostic.addCommand( "check-imports", CheckImports, "check ViDE's imports" )

        self.addHelpCommand()
        self.addExitCommand()

    def setVerbosity( self, verbosity ):
        Log.level = verbosity
