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
    return [ Project.inProgress.createOrRetrieve( CPlusPlus.Header, header ) for header in headers ]

def Sources( sources ):
    return [ Project.inProgress.createOrRetrieve( CPlusPlus.Source, source ) for source in sources ]

def Objects( sources, localLibraries ):
    return [ Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.CPlusPlus.Object, source, localLibraries ) for source in sources ]

def Executable( name, sources, localLibraries = [] ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.Binary.Executable, name, Objects( Sources( sources ), localLibraries ), localLibraries )

def DynamicLibrary( name, headers, sources, localLibraries = [] ):
    binary = Project.inProgress.buildkit.Binary.DynamicLibraryBinary( Project.inProgress.buildkit, name, Objects( Sources( sources ), localLibraries ) )
    return Project.inProgress.createOrRetrieve( Binary.DynamicLibrary, name, Headers( headers ), binary )
