import os.path
import py_compile

import ActionTree

from ViDE.Core import SubprocessFoo as Subprocess
from ViDE.Project.Artifacts.BasicArtifacts import MonofileInputArtifact, CopiedArtifact, AtomicArtifact, CompoundArtifact
from ViDE.Project.Artifacts.Binary import LinkedBinary

class Source( MonofileInputArtifact ):
    pass

class Script( CopiedArtifact ):
    def __init__( self, context, source, explicit ):
        self.__fileName = context.fileName( "bin", os.path.basename( source.getFileName() ) )
        CopiedArtifact.__init__(
            self,
            context,
            name = self.__fileName,
            source = source,
            destination = self.__fileName,
            explicit = explicit
        )

    def run( self, arguments ):
        Subprocess.execute( [ "python", self.__fileName ] + arguments, context = self.context, silent = True )

    def debug( self, arguments ):
        Subprocess.execute( [ "python", "-mpdb", self.__fileName ] + arguments, context = self.context )

    def getFileName( self ):
        return self.__fileName

class PythonCompileAction(ActionTree.Action):
    def __init__( self, source, destination ):
        self.__source = source
        self.__destination = destination
        ActionTree.Action.__init__(self, self.__compile, "python -m py_compile " + source)

    def __compile( self ):
        py_compile.compile( self.__source, self.__destination )

class Module( AtomicArtifact ):
    def __init__( self, context, source, strip, explicit ):
        self.__fileName = context.fileName( "pyd", strip( source.getFileName() ) + "c" )
        self.__source = source
        AtomicArtifact.__init__(
            self,
            context = context,
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
    def __init__( self, context, name, modules, explicit ):
        CompoundArtifact.__init__(
            self,
            context = context,
            name = name,
            componants = modules,
            explicit = explicit
        )

class CModule( LinkedBinary ):
    pass
