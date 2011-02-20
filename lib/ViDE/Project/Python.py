import os.path
import py_compile

from ViDE.Core.Action import Action
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Project.BasicArtifacts import MonofileInputArtifact, CopiedArtifact

class Source( MonofileInputArtifact ):
    pass

class Script( CopiedArtifact ):
    @staticmethod
    def computeName(  buildkit, source, explicit ):
        return buildkit.fileName( "bin", os.path.basename( source.getFileName() ) )

    def __init__( self, buildkit, source, explicit ):
        fileName = buildkit.fileName( "bin", os.path.basename( source.getFileName() ) )
        CopiedArtifact.__init__(
            self,
            buildkit,
            name = fileName,
            source = source,
            destination = fileName,
            explicit = explicit
        )

class PythonCompileAction( Action ):
    def __init__( self, source, destination ):
        self.__source = source
        self.__destination = destination
        Action.__init__( self )

    def doExecute( self ):
        py_compile.compile( self.__source, self.__destination )

    def computePreview( self ):
        return "python -m py_compile " + self.__source

class Module( AtomicArtifact ):
    @staticmethod
    def computeName( buildkit, source, strip, explicit ):
        return strip( source.getFileName() ) + "c"

    def __init__( self, buildkit, source, strip, explicit ):
        self.__fileName = buildkit.fileName( "pyd", strip( source.getFileName() ) + "c" )
        self.__source = source
        AtomicArtifact.__init__(
            self,
            name = self.__fileName,
            files = [ self.__fileName ],
            strongDependencies = [ source ],
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

    def doGetProductionAction( self ):
        return PythonCompileAction( self.__source.getFileName(), self.__fileName )

class Package( CompoundArtifact ):
    @staticmethod
    def computeName( buildkit, name, modules, explicit ):
        return name

    def __init__( self, buildkit, name, modules, explicit ):
        CompoundArtifact.__init__(
            self,
            name = name,
            componants = modules,
            explicit = explicit
        )

# class CModule:
    # pass
