from ViDE.Project.Project import Project
from ViDE.Project.Description.Utilities import *
from ViDE.Project.Description.Binary import __Executable
from ViDE.Project.Artifacts import CPlusPlus, Binary

def __CppHeader( header, explicit = False ):
    if isArtifact( header ):
        return header
    else:
        return Project.inProgress.createOrRetrieve( CPlusPlus.Header, header, explicit )

def __CppHeaders( headers ):
    return [ __CppHeader( header ) for header in headers ]

def __CppSource( source, explicit = False ):
    if isArtifact( source ):
        return source
    else:
        return Project.inProgress.createOrRetrieve( CPlusPlus.Source, source, explicit )

def __CppSources( sources ):
    return [ __CppSource( source ) for source in sources ]

def __CppObject( source, additionalDefines, localLibraries, explicit = False ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.CPlusPlus.Object, source, additionalDefines, localLibraries, explicit )

def __CppObjects( sources, objects, additionalDefines, localLibraries ):
    return objects + [ __CppObject( source, additionalDefines, localLibraries ) for source in sources ]

def CppHeader( header ):
    return __CppHeader( header, True )

def CppSource( source ):
    return __CppSource( source, True )

def CppObject( source, additionalDefines = [], localLibraries = [] ):
    return __CppObject( __CppSource( source, False ), additionalDefines, localLibraries, True )

def CppExecutable( name, sources = [], objects = [], localLibraries = [] ):
    return __Executable( name, __CppObjects( __CppSources( sources ), objects, [], localLibraries ), localLibraries, True )

def CppDynamicLibrary( name, headers, sources = [], objects = [], localLibraries = [], stripHeaders = identity ):
    binary = Project.inProgress.buildkit.Binary.DynamicLibraryBinary( Project.inProgress.buildkit, name, __CppObjects( __CppSources( sources ), objects, [ "BUILD_" + name.upper() ], localLibraries ), localLibraries, False )
    return Project.inProgress.createOrRetrieve( Binary.DynamicLibrary, name, __CppHeaders( headers ), binary, localLibraries, stripHeaders, True )

def CppStaticLibrary( name, headers, sources = [], objects = [], localLibraries = [], stripHeaders = identity ):
    binary = Project.inProgress.buildkit.Binary.StaticLibraryBinary( Project.inProgress.buildkit, name, __CppObjects( __CppSources( sources ), objects, [], localLibraries ), localLibraries, False )
    return Project.inProgress.createOrRetrieve( Binary.StaticLibrary, name, __CppHeaders( headers ), binary, localLibraries, stripHeaders, True )

def CppHeaderLibrary( name, headers, localLibraries = [], stripHeaders = identity ):
    return Project.inProgress.createOrRetrieve( Binary.HeaderLibrary, name, __CppHeaders( headers ), localLibraries, stripHeaders, True )
