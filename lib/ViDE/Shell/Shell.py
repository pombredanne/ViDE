from Misc import InteractiveCommandLineProgram

from ViDE import Log
from ViDE.Shell.AutoTest import AutoTest
from ViDE.Shell.Make import Make
from ViDE.Shell.Run import Run
from ViDE.Shell.Debug import Debug
from ViDE.Shell.Valgrind import Valgrind
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

        generation = self.createCommandGroup( "Artifact generation", "" )
        generation.addCommand( "make", Make, "build the project" )
        
        running = self.createCommandGroup( "Executable artifact running", "" )
        running.addCommand( "run", Run, "run an executable file" )
        running.addCommand( "debug", Debug, "debug an executable file" )
        running.addCommand( "valgrind", Valgrind, "run an executable file in valgrind" )

        self.addCommand( "install-tools", InstallTools, "install tools" )

        autodiagnostic = self.createCommandGroup( "ViDE's auto diagnostic", "" )
        autodiagnostic.addCommand( "autotest", AutoTest, "run ViDE's own unit tests" )
        autodiagnostic.addCommand( "check-imports", CheckImports, "check ViDE's imports" )

        self.addHelpCommand()
        self.addExitCommand()

    def setVerbosity( self, verbosity ):
        Log.level = verbosity
