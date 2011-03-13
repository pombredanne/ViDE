from ViDE.Project.Project import Project
from ViDE.Project.Artifacts import Binary

def __Executable( name, objects, localLibraries, externalLibraries, explicit = False ):
    return Project.inProgress.createArtifact( Project.inProgress.buildkit.Binary.Executable, name, objects, localLibraries, externalLibraries, explicit )

def Executable( name, objects = [], localLibraries = [], externalLibraries = [] ):
    return __Executable( name, objects, localLibraries, externalLibraries, True )
