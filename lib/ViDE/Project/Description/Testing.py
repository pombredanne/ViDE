from ViDE.Project.Project import Project
from ViDE.Project.Artifacts import Testing

def UnitTest( executable, additionalDependencies ):
    return Project.inProgress.createArtifact( Testing.UnitTest, executable, additionalDependencies, True )
