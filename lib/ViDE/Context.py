from ViDE.Buildkit import Buildkit
from ViDE.Toolset import Toolset
from ViDE.Project import Project

class Context:
    def __init__( self, program ):
        self.bk = Buildkit.load( program.buildkit )
        self.ts = Toolset.load( program.toolset )
        try:
            self.pj = Project.load( self )
        except IOError:
            pass
