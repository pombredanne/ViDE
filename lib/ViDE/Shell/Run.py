from CommandWithContext import CommandWithContext

from ViDE.Context import Context

class Run( CommandWithContext ):
    def executeWithContext( self, context, args ):
        artifact = context.project.retrieveByName( args[0] )
        if not hasattr( artifact, "run" ):
            artifact = context.project.retrieveByFile( context.fileName( "bin", args[0] ) )
        artifact.run( args[ 1: ] )
