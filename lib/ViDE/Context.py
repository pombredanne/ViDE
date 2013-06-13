import os.path

from ViDE.Platform import Platform
from ViDE.Buildkit import Buildkit
from ViDE.Flavour import Flavour
from ViDE.Toolset import Toolset
from ViDE.Project import Project

class Context:
    def __init__( self, program ):
        self.hostPlatform = Platform.load( program.hostPlatform, self )
        self.targetPlatform = Platform.load( program.targetPlatform, self )
        self.buildkit = Buildkit.load( program.buildkit, self )
        self.flavour = Flavour.load( program.flavour, self )
        self.toolset = Toolset.load( program.toolset, self )
        try:
            self.project = Project.load( self )
        except IOError:
            pass

    def fileName( self, *names ):
        return os.path.join(
            "build",
            "BuiltOn" + self.hostPlatform.name,
            "Targeting" + self.targetPlatform.name,
            "BuiltBy" + self.buildkit.name,
            self.flavour.name,
            *names
        )
