from Misc import InteractiveCommandLineProgram as ICLP

from ViDE.Context import Context

class CommandWithContext( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        
        toolsChoice = self.createOptionGroup( "Tools choice", "" )

        self.hostPlatform = ""

        self.targetPlatform = ""
        toolsChoice.addOption( [ "target" ], "targetPlatform", ICLP.StoreArgument( "PLATFORM" ), "target platform PLATFORM", ICLP.StoreConstant( "" ), "target current platform" )

        self.toolset = ""
        # toolsChoice.addOption( [ "t", "toolset" ], "toolset", ICLP.StoreArgument( "TOOLSET" ), "use toolset TOOLSET", ICLP.StoreConstant( "" ), "use default toolset" )

        self.buildkit = ""
        toolsChoice.addOption( [ "b", "buildkit" ], "buildkit", ICLP.StoreArgument( "BUILDKIT" ), "use buildkit BUILDKIT", ICLP.StoreConstant( "" ), "use default buildkit" )

        self.flavour = ""
        toolsChoice.addOption( [ "f", "flavour" ], "flavour", ICLP.StoreArgument( "FLAVOUR" ), "use flavour FLAVOUR", ICLP.StoreConstant( "" ), "use default flavour" )

    def execute( self, args ):
        context = Context( self )
        self.executeWithContext( context, args )
