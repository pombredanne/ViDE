from ViDE.Project.Project import Project
from ViDE.Project import Binary, CPlusPlus

def Executable( name, sources, localLibraries = [] ):
    sourceArtifacts = []
    for source in sources:
        sourceArtifacts.append( CPlusPlus.Source( source ) )

    objects = []
    for sourceArtifact in sourceArtifacts:
        objects.append( CPlusPlus.Object( sourceArtifact ) )

    executable = Binary.Executable( name, objects, localLibraries )
    Project.inProgress.addArtifact( executable )
    return executable

def DynamicLibrary( name, sources ):
    sourceArtifacts = []
    for source in sources:
        sourceArtifacts.append( CPlusPlus.Source( source ) )

    objects = []
    for sourceArtifact in sourceArtifacts:
        objects.append( CPlusPlus.Object( sourceArtifact ) )

    library = Binary.DynamicLibrary( name, objects )
    Project.inProgress.addArtifact( library )
    return library
