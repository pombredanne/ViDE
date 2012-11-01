from ViDE.Project.Project import Project
from ViDE.Project.Artifacts import Testing

def UnitTest( executable ):
    return Project.inProgress.createArtifact( Testing.UnitTest, executable, True )
