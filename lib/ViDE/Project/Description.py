from ViDE.Project.Project import Project
from ViDE.Project import Binary, CPlusPlus

def Objects( sources, localLibraries ):
    sourceArtifacts = []
    for source in sources:
        sourceArtifact = CPlusPlus.Source( source )
        Project.inProgress.addArtifact( sourceArtifact )
        sourceArtifacts.append( sourceArtifact )

    objects = []
    for sourceArtifact in sourceArtifacts:
        object = CPlusPlus.Object( sourceArtifact, localLibraries )
        Project.inProgress.addArtifact( object )
        objects.append( object )

    return objects

def Executable( name, sources, localLibraries = [] ):
    executable = Binary.Executable( name, Objects( sources, localLibraries ), localLibraries )
    Project.inProgress.addArtifact( executable )
    return executable

def DynamicLibrary( name, sources, localLibraries = [] ):
    library = Binary.DynamicLibrary( name, Objects( sources, localLibraries ) )
    Project.inProgress.addArtifact( library )
    return library
