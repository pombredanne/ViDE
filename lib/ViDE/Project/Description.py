from ViDE.Project.Project import Project
from ViDE.Project import Binary, CPlusPlus

def Executable( name, sources, objects = [] ):
    sourceArtifacts = []
    for source in sources:
        sourceArtifacts.append( CPlusPlus.Source( source ) )

    objects = []
    for sourceArtifact in sourceArtifacts:
        objects.append( CPlusPlus.Object( sourceArtifact ) )

    executable = Binary.Executable( name, objects )
    Project.inProgress.addArtifact( executable )
    return executable
