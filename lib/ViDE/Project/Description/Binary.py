from ViDE.Project.Project import Project
from ViDE.Project.Artifacts import Binary

def __Executable( name, objects, localLibraries, explicit = False ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.Binary.Executable, name, objects, localLibraries, explicit )

def Executable( name, objects = [], localLibraries = [] ):
    return __Executable( name, objects, localLibraries, True )
