import glob
import os
import fnmatch

from ViDE.Project.Project import Project
from ViDE.Project import Binary, CPlusPlus

def __AllXxxIn_flat( directory, xxx ):
    return glob.glob( os.path.join( directory, "*." + xxx ) )

def __AllXxxIn_recursive( directory, xxx ):
    l = []
    for path, dirs, files in os.walk( directory ):
        for fileName in fnmatch.filter( files, "*." + xxx ):
            l.append( os.path.join( path, fileName ) )
    return l

def AllXxxIn( directory, xxx, recursive ):
    if recursive:
        return __AllXxxIn_recursive( directory, xxx )
    else:
        return __AllXxxIn_flat( directory, xxx )

def AllCppIn( directory, recursive = True ):
    return AllXxxIn( directory, "cpp", recursive ) + AllXxxIn( directory, "c", recursive )

def AllHppIn( directory, recursive = True ):
    return AllXxxIn( directory, "hpp", recursive ) + AllXxxIn( directory, "h", recursive )

def AllIppIn( directory, recursive = True ):
    return AllXxxIn( directory, "ipp", recursive )

def AllPyIn( directory, recursive = True ):
    return AllXxxIn( directory, "py", recursive )

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
    executable = Project.inProgress.buildKit.Binary.Executable( name, Objects( Sources( sources ), localLibraries ), localLibraries )
    Project.inProgress.addArtifact( executable )
    return executable

def DynamicLibrary( name, headers, sources, localLibraries = [] ):
    binary = Project.inProgress.buildKit.Binary.DynamicLibraryBinary( name, Objects( Sources( sources ), localLibraries ) )
    library = Binary.DynamicLibrary( name, Headers( headers ), binary )
    Project.inProgress.addArtifact( library )
    return library
