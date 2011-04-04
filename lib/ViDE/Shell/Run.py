from Misc import InteractiveCommandLineProgram as ICLP

from ViDE.Context import Context

class Run( ICLP.Command ):
    def execute( self, args ):
        context = Context( self.program )
        artifact = context.project.retrieveByName( args[0] )
        if not hasattr( artifact, "run" ):
            artifact = context.project.retrieveByFile( context.buildkit.fileName( "bin", args[0] ) )
        artifact.run( args[ 1: ] )
