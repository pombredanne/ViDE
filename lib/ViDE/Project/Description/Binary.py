from ViDE.Project.Project import Project
from ViDE.Project.Artifacts import Binary

def Executable( name, objects = [], localLibraries = [] ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.Binary.Executable, name, objects, localLibraries, True )
