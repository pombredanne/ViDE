from Misc import InteractiveCommandLineProgram

from ViDE.Project.Project import Project

class Draw( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )

    def execute( self, args ):
        print Project.load( "videfile.py" ).getGraph().dotString()
