import os.path

from ViDE.Core.Action import Action
from ViDE.Project.Artifacts.BasicArtifacts import AtomicArtifact

class UnitTestAction( Action ):
    def __init__( self, executable, sentinel ):
        self.__executable = executable
        self.__sentinel = sentinel
        Action.__init__( self )

    def doExecute( self ):
        self.__executable.run( [] )
        open( self.__sentinel, "w" ).close()

    def computePreview( self ):
        return self.__executable.getFileName()

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
