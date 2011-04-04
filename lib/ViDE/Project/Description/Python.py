import sys

import ViDE
from ViDE.Project.Project import Project
from ViDE.Project.Description.Utilities import *
from ViDE.Project.Description.CPlusPlus import __CppObjects, __CppSources
from ViDE.Project.Artifacts import Python

sys.path.append( ViDE.toolsetsDirectory() )
import Tools
sys.path.pop()

def __PythonSource( source, explicit = False ):
    if isArtifact( source ):
        return source
    else:
        return Project.inProgress.createArtifact( Python.Source, source, explicit )

def __PythonSources( sources ):
    return [ __PythonSource( source ) for source in sources ]

def __PythonModule( source, strip, explicit = False ):
    return Project.inProgress.createArtifact( Python.Module, __PythonSource( source ), strip, explicit )

def __PythonModules( sources, modules, strip ):
    return modules + [ __PythonModule( source, strip ) for source in sources ]

def PythonSource( source ):
    return __PythonSource( source, True )

def PythonModule( source, strip = identity ):
    return __PythonModule( source, strip, True )

def PythonPackage( name, sources = [], modules = [], strip = identity ):
    return Project.inProgress.createArtifact( Python.Package, name, __PythonModules( __PythonSources( sources ), modules, strip ), True )

def PythonScript( source ):
    return Project.inProgress.createArtifact( Python.Script, __PythonSource( source ), True )

def CppPythonModule( name, sources = [], objects = [], localLibraries = [], externalLibraries = [] ):
    externalLibraries.append( Tools.Python.Python )
    return Project.inProgress.createArtifact( Project.inProgress.context.buildkit.Python.CModule, name, __CppObjects( __CppSources( sources ), objects, [], localLibraries, externalLibraries ), localLibraries, externalLibraries, True )
