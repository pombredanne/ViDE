from ViDE.Project.Project import Project
from ViDE.Project.Description.Utilities import *
from ViDE.Project.Description.Binary import __Executable
from ViDE.Project.Artifacts import Fortran

def __FortranSource( source, explicit = False ):
    if isArtifact( source ):
        return source
    else:
        return Project.inProgress.createArtifact( Fortran.Source, source, explicit )

def __FortranSources( sources ):
    return [ __FortranSource( source ) for source in sources ]

def __FortranObject( source, explicit = False ):
    return Project.inProgress.createArtifact( Project.inProgress.buildkit.Fortran.Object, source, explicit )

def __FortranObjects( sources, objects,  ):
    return objects + [ __FortranObject( source ) for source in sources ]

def FortranSource( source ):
    return __FortranSource( source, True )

def FortranObject( source, additionalDefines = [] ):
    return __FortranObject( __FortranSource( source, False ), True )

def FortranExecutable( name, sources = [], objects = [], localLibraries = [] ):
    return __Executable( name, __FortranObjects( __FortranSources( sources ), objects ), localLibraries, True )
