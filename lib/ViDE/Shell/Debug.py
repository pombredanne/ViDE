import os

import cairo

from Misc import InteractiveCommandLineProgram as ICLP
from ViDE.Buildkit import Buildkit
from ViDE.Toolset import Toolset
from ViDE.Project.Project import Project

import ViDE
from ViDE import Log

class Debug( ICLP.Command ):
    def __init__( self, program ):
        ICLP.Command.__init__( self, program )

    def execute( self, args ):
        buildkit = Buildkit.load( self.program.buildkit, "debug" )
        toolset = Toolset.load( self.program.toolset )
        project = Project.load( buildkit, toolset )
        artifact =  project.retrieveByName( args[0] )
        if not hasattr( artifact, "debug" ):
            artifact =  project.retrieveByFile( buildkit.fileName( "bin", args[0] ) )
        artifact.debug( args[ 1: ] )
