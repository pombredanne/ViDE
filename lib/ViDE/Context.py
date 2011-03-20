from ViDE.Buildkit import Buildkit
from ViDE.Toolset import Toolset
from ViDE.Project import Project

class Context:
    def __init__( self, program ):
        self.buildkit = Buildkit.load( program.buildkit, self )
        self.toolset = Toolset.load( program.toolset, self )
        try:
            self.project = Project.load( self )
        except IOError:
            pass
