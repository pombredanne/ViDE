from ViDE.Project.Project import Project
from ViDE.Project import Binary, CPlusPlus

def Headers( headers ):
    headerArtifacts = []
    for header in headers:
        headerArtifact = CPlusPlus.Header( header )
        Project.inProgress.addArtifact( headerArtifact )
        headerArtifacts.append( headerArtifact )
    return headerArtifacts

def Sources( sources ):
    sourceArtifacts = []
    for source in sources:
        sourceArtifact = CPlusPlus.Source( source )
        Project.inProgress.addArtifact( sourceArtifact )
        sourceArtifacts.append( sourceArtifact )
    return sourceArtifacts

def Objects( sources, localLibraries ):
    objects = []
    for source in sources:
        object = Project.inProgress.buildKit.CPlusPlus.Object( source, localLibraries )
        Project.inProgress.addArtifact( object )
        objects.append( object )
    return objects

def Executable( name, sources, localLibraries = [] ):
    executable = Binary.Executable( name, Objects( Sources( sources ), localLibraries ), localLibraries )
    Project.inProgress.addArtifact( executable )
    return executable

def DynamicLibrary( name, headers, sources, localLibraries = [] ):
    library = Binary.DynamicLibrary( name, Headers( headers ), Objects( Sources( sources ), localLibraries ) )
    Project.inProgress.addArtifact( library )
    return library
