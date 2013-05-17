# Standard library
import os.path

# Third-party libraries
import ActionTree

# Project
from ViDE.Project.Artifacts.BasicArtifacts import AtomicArtifact


### @todo Maybe remove this thin and useless class (__execute could be a method of class UnitTest)
class UnitTestAction(ActionTree.Action):
    def __init__( self, executable, sentinel ):
        self.__executable = executable
        self.__sentinel = sentinel
        Action.__init__(self, self.__execute, executable.getFileName())

    def __execute( self ):
        self.__executable.run( [] )
        open( self.__sentinel, "w" ).close()


class UnitTest( AtomicArtifact ):
    def __init__( self, context, executable, additionalDependencies, explicit ):
        self.__fileName = context.fileName( "test", os.path.basename( executable.getFileName() ) + ".ok" )
        self.__executable = executable
        AtomicArtifact.__init__(
            self,
            context = context,
            name = self.__fileName,
            files = [ self.__fileName ],
            strongDependencies = [ executable ] + additionalDependencies,
            orderOnlyDependencies = [],
            automaticDependencies = [],
            explicit = explicit
        )

    def doGetProductionAction( self ):
        return UnitTestAction( self.__executable, self.__fileName )
