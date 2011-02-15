from Misc import InteractiveCommandLineProgram

import ViDE
from ViDE.Project.Project import Project
from ViDE.Buildkit import Buildkit

class Draw( InteractiveCommandLineProgram.Command ):
    def __init__( self, program ):
        InteractiveCommandLineProgram.Command.__init__( self, program )
        ### @todo Add an option to not call dot, and -T -O options, to be forwarded to dot
        ### @todo Add a positional argument to choose what to draw: project's artifacts graph, ViDe's dependency graph, project's action graph project's include/import graph
        ### We may have to use something else than dot for some drawings
        ### @todo Transfert the project's action graph from command Make to here
        
    def execute( self, args ):
        buildkit = Buildkit.load( self.program.buildkit )
        project = Project.load( buildkit )
        ### @todo Call dot
        print project.getGraph().dotString()
