from CommandWithContext import CommandWithContext

from ViDE.Context import Context

class Debug( CommandWithContext ):
    def executeWithContext( self, context, args ):
        artifact =  context.project.retrieveByName( args[0] )
        if not hasattr( artifact, "debug" ):
            artifact =  project.retrieveByFile( context.fileName( "bin", args[0] ) )
        artifact.debug( args[ 1: ] )
