from Misc import InteractiveCommandLineProgram as ICLP

from ViDE.Context import Context

class Run( ICLP.Command ):
    def execute( self, args ):
        context = Context( self.program )
        artifact =  context.pj.retrieveByName( args[0] )
        if not hasattr( artifact, "run" ):
            artifact =  project.retrieveByFile( context.bk.fileName( "bin", args[0] ) )
        artifact.run( args[ 1: ] )
