from ViDE.Project.Project import Project
from ViDE.Project.Description.Utilities import *
from ViDE.Project.Description.Binary import __Executable
from ViDE.Project.Artifacts import CPlusPlus, Binary

def __CppHeader( header, explicit = False ):
    if isArtifact( header ):
        return header
    else:
        return Project.inProgress.createArtifact( CPlusPlus.Header, header, explicit )

def __CppHeaders( headers ):
    return [ __CppHeader( header ) for header in headers ]

def __CppSource( source, explicit = False ):
    if isArtifact( source ):
        return source
    else:
        return Project.inProgress.createArtifact( CPlusPlus.Source, source, explicit )

def __CppSources( sources ):
    return [ __CppSource( source ) for source in sources ]

def __CppObject( source, additionalDefines, localLibraries, externalLibraries, explicit = False ):
    return Project.inProgress.createArtifact( Project.inProgress.context.bk.CPlusPlus.Object, source, additionalDefines, localLibraries, externalLibraries, explicit )

def __CppObjects( sources, objects, additionalDefines, localLibraries, externalLibraries ):
    return objects + [ __CppObject( source, additionalDefines, localLibraries, externalLibraries ) for source in sources ]

def CppHeader( header ):
    return __CppHeader( header, True )

def CppSource( source ):
    return __CppSource( source, True )

def CppObject( source, additionalDefines = [], localLibraries = [], externalLibraries = [] ):
    return __CppObject( __CppSource( source, False ), additionalDefines, localLibraries, externalLibraries, True )

def CppExecutable( name, sources = [], objects = [], localLibraries = [], externalLibraries = [] ):
    return __Executable( name, __CppObjects( __CppSources( sources ), objects, [], localLibraries, externalLibraries ), localLibraries, externalLibraries, True )

def CppDynamicLibrary( name, headers, sources = [], objects = [], localLibraries = [], externalLibraries = [], stripHeaders = identity ):
    headers = __CppHeaders( headers )
    binary = Project.inProgress.context.bk.Binary.DynamicLibraryBinary( Project.inProgress.context, name, __CppObjects( __CppSources( sources ), objects, [ "BUILD_" + name.upper() ], localLibraries, externalLibraries ), localLibraries, externalLibraries, False )
    return Project.inProgress.createArtifact( Binary.DynamicLibrary, name, headers, binary, localLibraries, externalLibraries, stripHeaders, True )

def CppStaticLibrary( name, headers, sources = [], objects = [], localLibraries = [], externalLibraries = [], stripHeaders = identity ):
    headers = __CppHeaders( headers )
    binary = Project.inProgress.context.bk.Binary.StaticLibraryBinary( Project.inProgress.context, name, __CppObjects( __CppSources( sources ), objects, [], localLibraries, externalLibraries ), localLibraries, externalLibraries, False )
    return Project.inProgress.createArtifact( Binary.StaticLibrary, name, headers, binary, localLibraries, externalLibraries, stripHeaders, True )

def CppHeaderLibrary( name, headers, localLibraries = [], externalLibraries = [], stripHeaders = identity ):
    return Project.inProgress.createArtifact( Binary.HeaderLibrary, name, __CppHeaders( headers ), localLibraries, externalLibraries, stripHeaders, True )
