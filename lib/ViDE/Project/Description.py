from ViDE.Project.Project import Project
from ViDE.Project import Binary

def Executable( name, sources ):
    Project.inProgress.addArtifact( Binary.Executable( name ) )
