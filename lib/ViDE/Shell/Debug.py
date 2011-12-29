from Misc import InteractiveCommandLineProgram as ICLP

from ViDE.Context import Context

class Debug( ICLP.Command ):
    def execute( self, args ):
        context = Context( self.program )
        artifact =  context.project.retrieveByName( args[0] )
        if not hasattr( artifact, "debug" ):
            artifact =  project.retrieveByFile( context.fileName( "bin", args[0] ) )
        artifact.debug( args[ 1: ] )
