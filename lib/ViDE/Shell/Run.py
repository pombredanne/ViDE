import subprocess
import os

import cairo

from Misc import InteractiveCommandLineProgram as ICLP
from ViDE.Buildkit import Buildkit

import ViDE
from ViDE import Log

class Run( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )
        
    def execute( self, args ):
        buildkit = Buildkit.load( self.program.buildkit )
        self.__updateEnvironment( buildkit.getExecutionEnvironment() )
        self.__updateEnvironment( { "PYTHONPATH" : buildkit.fileName( "pyd" ) } )
        subprocess.check_call( args )

    def __updateEnvironment( self, updates ):
        for k in updates:
            os.environ[ k ] = updates[ k ]
