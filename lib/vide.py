import Misc.InteractiveCommandLineProgram as InteractiveCommandLineProgram

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
        verbosity.addOption( "quiet", "verbosity", InteractiveCommandLineProgram.StoreConstant( 0 ), "print as few messages as possible", InteractiveCommandLineProgram.StoreConstant( 1 ), "print normal messages" )
        verbosity.addOption( "verbose", "verbosity", InteractiveCommandLineProgram.StoreConstant( 2 ), "print information messages", InteractiveCommandLineProgram.StoreConstant( 1 ), "don't print information messages" )
        verbosity.addOption( "debug", "verbosity", InteractiveCommandLineProgram.StoreConstant( 3 ), "print debug messages", InteractiveCommandLineProgram.StoreConstant( 1 ), "don't print debug messages" )

        toolsChoice = self.createOptionGroup( "Tools choice", "" )
        self.toolset = defaultToolset
        toolsChoice.addOption( "toolset", "toolset", InteractiveCommandLineProgram.StoreArgument( "TOOLSET" ), "use toolset TOOLSET", InteractiveCommandLineProgram.StoreConstant( defaultToolset ), "use default toolset" )

        self.buildkit = defaultBuildkit
        toolsChoice.addOption( "buildkit", "buildkit", InteractiveCommandLineProgram.StoreArgument( "BUILDKIT" ), "use buildkit BUILDKIT", InteractiveCommandLineProgram.StoreConstant( defaultBuildkit ), "use default buildkit" )

        generation = self.createCommandGroup( "Artifact generation", "" )
        generation.addCommand( "make", DummyCommand( "Make" ), "build the project (compile, link, etc.)" )
        generation.addCommand( "compile", DummyCommand( "Compile" ), "compile project sources (no link edition)" )

        self.addHelpCommand()
        self.addExitCommand()

if __name__ == "__main__":
    Shell().execute()
