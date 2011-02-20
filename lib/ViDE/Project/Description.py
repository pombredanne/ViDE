import glob
import os
import fnmatch

from ViDE.Project.FindFiles import *
from ViDE.Project.Project import Project
from ViDE.Core.Artifact import Artifact
from ViDE.Project import Binary, CPlusPlus, Python

def identity( x ):
    return x

def __isArtifact( object ):
    return isinstance( object, Artifact )

def __Header( header, explicit = False ):
    if __isArtifact( header ):
        return header
    else:
        return Project.inProgress.createOrRetrieve( CPlusPlus.Header, header, explicit )

def __Headers( headers ):
    return [ __Header( header ) for header in headers ]

def __Source( source, explicit = False ):
    if __isArtifact( source ):
        return source
    else:
        return Project.inProgress.createOrRetrieve( CPlusPlus.Source, source, explicit )

def __Sources( sources ):
    return [ __Source( source ) for source in sources ]

def __Object( source, additionalDefines, localLibraries, explicit = False ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.CPlusPlus.Object, source, additionalDefines, localLibraries, explicit )

def __Objects( sources, objects, additionalDefines, localLibraries ):
    return objects + [ __Object( source, additionalDefines, localLibraries ) for source in sources ]

def Header( header ):
    return __Header( header, True )

def Source( source ):
    return __Source( source, True )

def Object( source, additionalDefines = [], localLibraries = [] ):
    return __Object( __Source( source, False ), additionalDefines, localLibraries, True )

def Executable( name, sources = [], objects = [], localLibraries = [] ):
    return Project.inProgress.createOrRetrieve( Project.inProgress.buildkit.Binary.Executable, name, __Objects( __Sources( sources ), objects, [], localLibraries ), localLibraries, True )

def DynamicLibrary( name, headers, sources = [], objects = [], localLibraries = [], stripHeaders = identity ):
    binary = Project.inProgress.buildkit.Binary.DynamicLibraryBinary( Project.inProgress.buildkit, name, __Objects( __Sources( sources ), objects, [ "BUILD_" + name.upper() ], localLibraries ), localLibraries, False )
    return Project.inProgress.createOrRetrieve( Binary.DynamicLibrary, name, __Headers( headers ), binary, localLibraries, stripHeaders, True )

def StaticLibrary( name, headers, sources = [], objects = [], localLibraries = [], stripHeaders = identity ):
    binary = Project.inProgress.buildkit.Binary.StaticLibraryBinary( Project.inProgress.buildkit, name, __Objects( __Sources( sources ), objects, [], localLibraries ), localLibraries, False )
    return Project.inProgress.createOrRetrieve( Binary.StaticLibrary, name, __Headers( headers ), binary, localLibraries, stripHeaders, True )

def HeaderLibrary( name, headers, localLibraries = [], stripHeaders = identity ):
    return Project.inProgress.createOrRetrieve( Binary.HeaderLibrary, name, __Headers( headers ), localLibraries, stripHeaders, True )

def __PythonSource( source, explicit = False ):
    if __isArtifact( source ):
        return source
    else:
        return Project.inProgress.createOrRetrieve( Python.Source, source, explicit )

def __PythonSources( sources ):
    return [ __PythonSource( source ) for source in sources ]

def __PythonModule( source, strip, explicit = False ):
    return Project.inProgress.createOrRetrieve( Python.Module, __PythonSource( source ), strip, explicit )

def __PythonModules( sources, strip ):
    return [ __PythonModule( source, strip ) for source in sources ]

def PythonSource( source ):
    return __PythonSource( source, True )

def PythonModule( source, strip = identity ):
    return __PythonModule( source, strip, True )

def PythonPackage( name, sources, strip = identity ):
    return Project.inProgress.createOrRetrieve( Python.Package, name, __PythonModules( __PythonSources( sources ), strip ), True )

def PythonScript( source ):
    return Project.inProgress.createOrRetrieve( Python.Script, __PythonSource( source ), True )
