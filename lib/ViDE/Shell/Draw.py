import imp
import os

from Misc import InteractiveCommandLineProgram

import ViDE
from ViDE.Project.Project import Project

class Draw( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )

    def execute( self, args ):
        buildKit = imp.load_source( self.program.buildkit, os.path.join( ViDE.buildKitsDirectory, self.program.buildkit + ".py" ) )
        print Project.load( "videfile.py", buildKit ).getGraph().dotString()
