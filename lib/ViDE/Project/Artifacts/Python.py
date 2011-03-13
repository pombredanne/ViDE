import os.path
import py_compile

from ViDE.Core import Subprocess
from ViDE.Core.Action import Action
from ViDE.Core.Artifact import AtomicArtifact, CompoundArtifact
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact, CopiedArtifact
from ViDE.Project.Artifacts.Binary import LinkedBinary

class Source( MonofileInputArtifact ):
    pass

class Script( CopiedArtifact ):
    def __init__( self, buildkit, source, explicit ):
        self.__fileName = buildkit.fileName( "bin", os.path.basename( source.getFileName() ) )
        self.__buildkit = buildkit
        CopiedArtifact.__init__(
            self,
            buildkit,
            name = self.__fileName,
            source = source,
            destination = self.__fileName,
            explicit = explicit
        )

    def run( self, arguments ):
        Subprocess.execute( [ "python", self.__fileName ] + arguments, buildkit = self.__buildkit )

    def debug( self, arguments ):
        Subprocess.execute( [ "python", "-mpdb", self.__fileName ] + arguments, buildkit = self.__buildkit )

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
    def __init__( self, buildkit, name, modules, explicit ):
        CompoundArtifact.__init__(
            self,
            name = name,
            componants = modules,
            explicit = explicit
        )

class CModule( LinkedBinary ):
    pass
