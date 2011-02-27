import subprocess
import os

import cairo

from Misc import InteractiveCommandLineProgram as ICLP
from ViDE.Buildkit import Buildkit
from ViDE.Project.Project import Project

import ViDE
from ViDE import Log

class Run( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )

    def execute( self, args ):
        buildkit = Buildkit.load( self.program.buildkit, self.program.flavour )
        project = Project.load( buildkit )
        artifact =  project.retrieveByName( args[0] )
        if not hasattr( artifact, "run" ):
            artifact =  project.retrieveByFile( buildkit.fileName( "bin", args[0] ) )
        artifact.run( args[ 1: ] )